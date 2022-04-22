# python_learning
Learning record of Python syntax and related libraries
# modules

01. Built-in Objects
    - exceptions – Built-in error classes
02. String Services
    - codecs – String encoding and decoding
    - difflib – Compare sequences
    - string – Working with text
    - StringIO and cStringIO – Work with text buffers using file-like API
    - re – Regular Expressions
    - struct – Working with Binary Data
    - textwrap – Formatting text paragraphs
03. Data Types
    - array – Sequence of fixed-type data
    - datetime – Date/time value manipulation
    - calendar – Work with dates
    - collections – Container data types
    - heapq – In-place heap sort algorithm
    - bisect – Maintain lists in sorted order
    - sched – Generic event scheduler.
    - Queue – A thread-safe FIFO implementation
    - weakref – Garbage-collectable references to objects
    - copy – Duplicate objects
    - pprint – Pretty-print data structures
04. Numeric and Mathematical Modules
    - decimal – Fixed and floating point math
    - fractions – Rational Numbers
    - functools – Tools for Manipulating Functions
    04. itertools – Iterator functions for efficient looping
    - math – Mathematical functions
    - operator – Functional interface to built-in operators
    - random – Pseudorandom number generators
05. Internet Data Handling
    - base64 – Encode binary data into ASCII characters
    - json – JavaScript Object Notation Serializer
    - mailbox – Access and manipulate email archives
    - mhlib – Work with MH mailboxes
06. File Formats
    - csv – Comma-separated value files
    - ConfigParser – Work with configuration files
    - robotparser – Internet spider access control
07. Cryptographic Services
    - hashlib – Cryptographic hashes and message digests
    - hmac – Cryptographic signature and verification of messages.
08. File and Directory Access
    01. os.path – Platform-independent manipulation of file names.
    - fileinput – Process lines from input streams
    - filecmp – Compare files
    - tempfile – Create temporary filesystem resources.
    - glob – Filename pattern matching
    - fnmatch – Compare filenames against Unix-style glob patterns.
    - linecache – Read text files efficiently
    08. shutil – High-level file operations.
    - dircache – Cache directory listings
09. Data Compression and Archiving
    - bz2 – bzip2 compression
    - gzip – Read and write GNU zip files
    - tarfile – Tar archive access
    - zipfile – Read and write ZIP archive files
    - zlib – Low-level access to GNU zlib compression library
10. Data Persistence
    - anydbm – Access to DBM-style databases
    - dbhash – DBM-style API for the BSD database library
    - dbm – Simple database interface
    - dumbdbm – Portable DBM Implementation
    - gdbm – GNU’s version of the dbm library
    06. pickle and cPickle – Python object serialization
    - shelve – Persistent storage of arbitrary Python objects
    - whichdb – Identify DBM-style database formats
    - sqlite3 – Embedded Relational Database
11. Generic Operating System Services
    - os – Portable access to operating system specific features.
    - time – Functions for manipulating clock time
    - getopt – Command line option parsing
    - optparse – Command line option parser to replace getopt.
    - argparse – Command line option and argument parsing.
    - logging – Report status, error, and informational messages.
    - getpass – Prompt the user for a password without echoing.
    - platform – Access system version information
12. Optional Operating System Services
    - threading – Manage concurrent threads
    - mmap – Memory-map files
    - multiprocessing – Manage processes like threads
    - readline – Interface to the GNU readline library
    - rlcompleter – Adds tab-completion to the interactive interpreter
13.Unix-specific Services
    - commands – Run external shell commands
    - grp – Unix Group Database
    - pipes – Unix shell command pipeline templates
    - pwd – Unix Password Database
    - resource – System resource management
14. Interprocess Communication and Networking
    - asynchat – Asynchronous protocol handler
    - asyncore – Asynchronous I/O handler
    - signal – Receive notification of asynchronous system events
    04. subprocess – Work with additional processes
15. Internet Protocols and Support
    - BaseHTTPServer – base classes for implementing web servers
    - cgitb – Detailed traceback reports
    - Cookie – HTTP Cookies
    - imaplib - IMAP4 client library
    - SimpleXMLRPCServer – Implements an XML-RPC server.
    - smtpd – Sample SMTP Servers
    - smtplib – Simple Mail Transfer Protocol client
    - socket – Network Communication
    - select – Wait for I/O Efficiently
    - SocketServer – Creating network servers.
    - urllib – simple interface for network resource access
    - urllib2 – Library for opening URLs.
    - urlparse – Split URL into component pieces.
    - uuid – Universally unique identifiers
    - webbrowser – Displays web pages
    - xmlrpclib – Client-side library for XML-RPC communication
16. Structured Markup Processing Tools
    - xml.etree.ElementTree – XML Manipulation API
17. Internationalization
    - gettext – Message Catalogs
    - locale – POSIX cultural localization API
18. Program Frameworks
    - cmd – Create line-oriented command processors
    - shlex – Lexical analysis of shell-style syntaxes.
19. Development Tools
    - doctest – Testing through documentation
    - pydoc – Online help for Python modules
    - unittest – Automated testing framework
    - pdb – Interactive Debugger
20. Debugging and Profiling
    - profile, cProfile, and pstats – Performance analysis of Python programs.
    - timeit – Time the execution of small bits of Python code.
    - trace – Follow Python statements as they are executed
21. Python Runtime Services
    - abc – Abstract Base Classes
    - atexit – Call functions when a program is closing down
    - contextlib – Context manager utilities
    - gc – Garbage Collector
    - inspect – Inspect live objects
    - site – Site-wide configuration
    - sys – System-specific Configuration
    - sysconfig – Interpreter Compile-time Configuration
    - traceback – Extract, format, and print exceptions and stack traces.
    - warnings – Non-fatal alerts
22. Python Language Services
    - compileall – Byte-compile Source Files
    - dis – Python Bytecode Disassembler
    - pyclbr – Python class browser support
    - tabnanny – Indentation validator
23. Importing Modules
    - imp – Interface to module import mechanism.
    - pkgutil – Package Utilities
    - zipimport – Load Python code from inside ZIP archives
24. Miscelaneous
    01. schedule:定时任务(支持多线程执行,可控制多线程数量)