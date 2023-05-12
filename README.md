# expertlead-logger

## General Considerations

Loggers are one of the most fundamental parts of a software project, they provide observability under normal
circumstances and are of critical importance in case of failures as often logs are the only insight available to
investigate unexpected software failures. For this reason they need to be simple, very very robust, and performant.
those features com in a specific order as we do not have a vay to observe failures in the actual logging process,
therefore we should be able to exclude it beforehand, robustness is paramount as the logger is one of the first
component of a system that needs to be available at startup, the last to be closed and we need to be sure all logs are
flushed even, and in particular, under conditions of abnormal progran termination. Therefore, I would warmly recommend
adopting a proper logging framework in any case where logging is needed.

In this specific case, given the goal of the exercise is assessing programming skills more than providing working code,
we'll relax some constraints and implement e.g. a producer consumer model.

## Requirements and Installation

The exercise is developed using python 3.10, it has close to no external requirements and should work out of the box. We
still provide a requirements.txt file and a setup.py file for sake of completeness.

Test are implemented using unittest and can be run from the test folder. The main.py module provides some very simple
demonstration of the logger initialization and its uses.

## Considerations on Principles, Design Patterns, and Implementation

In this exercise we are going to point out the SOLID principles Single Duty, Open Closeness, Liskov Substitution,
Interface Segregation, and Dependency inversion

As we can see, the logger has only one simple function, thus logging, this is clear from the interface expressed through
the use of an abstract class, as python does not provide a specific primitive for interfaces. The handlers are defined
to be open to extension and close to modification, to the extent allowed by the language. Liskov substitution in python
is easily achieved as python is a weakly typed language and any class is formally a valid replacement for any other. In
the specific case all we need to ensure if behavioural compatibility with the ancestor. Finally, the log handlers are
injected in the logger. This allows us to implement any flavour of logging handler for any type of output stream and
inject it as long as it implements a very simple interface i.e. it needs to expose log_level and log().

The logger orchestrates the log dispatcher and implements a Bridge
Pattern (https://en.wikipedia.org/wiki/Bridge_pattern), the actual implementations of the log handlers are injected.

IMPROVEMENT: In the specific case the log handler implementations are injected in constructor, further enhancement might
allow adding or removing log handlers at runtime.

### Producer Consumer Pattern

The AsyncLogHandler implements a producer/consumer pattern. Under normal circumstances I would recommend against this
approach for logging as in case of abrupt termination of the process we may lose part of the logs not consumed yet. A
better implementation might consider persisting the logs immediately and then tee the logs and forward them outside the
machine in a separate process (e.g. using fluentd daemon). the latter pattern is more robust as the external process is
less likely to fail and even in case of failure one can still fetch the logs from the local persistence device (e.g.
local disk). For logging, performance is hardly an issue and in cases of very, very high volumes of logs once can still
memory-map the file and rely on the operative system to persist the data even if the process terminates abruptly. The
low-weight feature of logging is clear from the timestamps as we can generate and print logs at sub-nanosecond rate.

The producer/consumer pattern is very simple, on startup the handler instantiates a blocking queue, the queue is thread
safe and synchronized. The init method also spawns one or more worker threads and lets the worker threads listen on the
queue. When the log method of the logger is invoked instead of persisting the message log immediately, it pushes the
message log on the queue. When the worker node is triggered by the presence of message logs in the queue, it consumes
the message logs and persists them. The main method in main.py shows the behaviour of the AsyncLogHandler under 2
different regimes. In the first case, the caller generates 3 logs in quick succession, the synchronous log handlers log
them immediately, while the Async log handler pushes them to the queue, and they are not visible on the console until
the worker threads take control and process them. When the logging volume is low (i.e. we add one second of delay
between logs), the worker thread is triggered more often and the logs appear in the expected order.

In python, the console is not thread safe. Therefore, when we have different threads concurrently printing to the
console, it can lead to interleaved log strings. To avoid this issue we implemented a Mock-Synchronized print function.
The function creates a critical section around the print function using a Mutex lock. Therefore, we can ensure only one
thread at a time has access to the print. The other threads trying to acquire the lock are left waiting outside the
critical section. The mutex if fully managed by the context and released after the context terminates. Use of a context
allows to dramatically reduce the boilerplate code required to release the resources, in particular in case of abnormal
execution e.g. in case something goes wrong with the persistence device, and we get an exception.  
To note, the pseudo-synchronization is mocking a persistence device and the synchronization works only for threads using
the sync_print function. Any other process using a normal print can access the console skipping the lock.

## Considerations on Performance

The logging process per-se is quite efficient, it is mostly in-memory and with few exception persistence is generally
offloaded to the operative system (traditional file-based logs) or simply disregarded under the assumption "something"
will capture the stdout (https://12factor.net/logs). Therefore, performance should not be of concern, unless there are
very specific reasons requiring to consider performance. If we abstract from the log problem, and we focus more on the
processing of streams of data, we might have to deal with large volumes of data to be processed. The solution to
performance issues in those cases has multiple aspects. Often it requires to be addressed at architectural level as a
reasonable estimation of the data volume can drive the architectural pattern one might want to implement and define a
range for the amount of infrastructure needed to stand the load. Once the volumes are reasonably defined one might want
to consider streaming single pieces of data, streaming (micro-)batches of data and process them together, or store the
data and stream events triggering distributed executors, which in turn fetch and process the data. The most common
Architectural Patterns use synchronous or asynchronous message brokers and often implement Reactor or Proactor patterns
to distribute the load on a constellation of distributed workers.

In the case os small scale in-memory log streaming, the first thing we can do to improve performance is moving from a
single-event processing to a batching strategy. I.e. more events are collected and processed together. The
AsyncLogHandler is posing the basis for this type of processing as the Queue acts as a buffer for the logs and once a
worker is activated it processes a good chunk of the logs in the queue before having to yield control. Use of multiple
workers and the use ForkAndMerge thread pool might allow to have a variable number of workers depending on the incoming
workload. In any case one needs ot be aware of the resources available as excessively increasing the number of workers
might starve the system for resources needed for the main computation.  

## Opportunities

Under normal circumstances I should have defined LogHandler.log() to be an abstract method as each logger should provide
its own implementation of logging to a specific device. In this specific case it was convenient to provide a unified
implementation as most mock loggers have exactly the same implementation, thus we are saving some copy/paste. Assuming
the log() method to be abstract, given the rest of the class is implemented, it would give rise to a Template
Pattern (https://en.wikipedia.org/wiki/Template_method_pattern). In the AsyncLogHandler we see how a concrete
implementation of the pattern should be implemented as it overrides the log method.

## Improvements, and How we can make Logger more open to modifications

The structure of the logger is already quite open to extension as it leverages dependency injection, and it implements a
bridge design Pattern. Therefore, it is agnostic to the handler's implementation, and it can accommodate any type of
handler as it is.

The format of message printed by the handlers is hardcoded, providing the facilities to inject a format string would
make it more flexible and allow providing different patterns for different loggers.

We could also extend the logger class to provide indication of what module of code is logging, so that we can help
log-analysis pointing at specific modules of code.

Another convenient enhancement to the logger is wrapping the configuration and instantiation of the logger in a Builder
Pattern (https://en.wikipedia.org/wiki/Builder_pattern) or in a Factory
Pattern (https://en.wikipedia.org/wiki/Factory_method_pattern), with the latter being particular convenient as it allows
to create a Singleton Instance of the logger and make it accessible to multiple threads, without having to duplicate
resources or handle contention. The Factory Pattern also allows to encapsulate the generation logic and provide a device
to instantiate a logger programmatically or using a configuration file, with the latter being quite convenient as the
number of features grow and the configuration gets more complex.

