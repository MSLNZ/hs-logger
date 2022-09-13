# hs_logger
This is the logger used by the MSL Humidity Standards team for calibrations and research. It is undergoing continuous improvement as part of BAU.

The logger has the following functionalities:
* Read and write to any instrument that has an {instrument}.json file using the instrument window of main_controller.py
* Log data for {job}.json files using the job window of main_controller.py
* Control jobs using an {autoprofile}.csv file on the Profile tab of the job window above
* Produce graphs of logged data
* Record files of logged data for later analysis

The software is started by running main_controller.py

***

# Instrument files
Instrument files consist of a dictionary containing at least the following details:
* instrument_id (STRING; The name the logger uses to refer to this instrument once it's imported)
* driver (STRING; What driver the instrument uses to read/write)
* operations  (DICTIONARY of (STRING: DICTIONARY of (STRING: VARIOUS)); Contents of this dictionary are listed below.)

Specific drivers may require additional information. For instance, the generic_driver_visa_serial driver requires a port number, baudrate, and write_ and read_termination characters. Documentation of what additional details are required is included in the drivers. (NB: This information isn't currently in the drivers. It should be added.)

The "operations" dictionary contains every command that can be given to the instrument. These are split into "read", "write", and "action". Each operation must contain the following:
* type (STRING; The first section of this string determines if this operation is a read, write, or action. Additional information here can be used by the driver, such as the read_multiple, read_store, and write_action commands detailed at the end of this section.)
* name (STRING; The plain text name for the command for use in documentation.)
* id (STRING; This should be the same as the key of this operation in the "operations" dictionary. It is the function that is called by the logger to perform this operation.)
* details (STRING; A description of this specific operation for use in documentation.)
* command (STRING; The command that communicates the desired operation to the device. Use "{}" in place of inputs in write commands.)

The following additional details are required if the operation is a read operation:
* transform_eq (LIST of (STRING,FLOAT,FLOAT,FLOAT,FLOAT); The equation used to generate the transformed data. The first datum can be used to tell certain drivers what equation the transform uses, such as "T" using a Callendar–Van Dusen equation. The next four numbers are the variables used in the transform equation. Defaults to ["V", 0, 1, 0 0])
* cal_freq (FLOAT; The frequency of required calibration, in years. A value of 0 means the operation does not need routine checking.)
* check_freq (FLOAT; The frequency of required checking, in years. A value of 0 means the operation does not need routine calibration.)
* cal_date (STRING; The date of the last valid calibration report for the particular operation, if appropriate. Defaults to "".)
* check_date (STRING; The date of the last valid check for the particular operation (such as an ice point check), if appropriate. Otherwise, Defaults to "".)
* uncertainty (FLOAT; The uncertainty associated with the operation, if appropriate. A value of 0 means the operation does not have an associated uncertainty.)

The following details are recommended if the operation is a write operation:
* check_set (STRING; The read operation that reads the value this operation writes to, if available. Defaults to "".)
* check_actual (STRING; The read operation that reads the transducer this operation would attempt to control, if available. Defaults to "".)

Some instruments use read_multiple/read_store commands or write_action commands. These are special functions that are detailed below.

read_multiple and read_store are connected commands that are used to speed up read/write times for instruments that allow them. This is accomplished by using a read_multiple operation to read a bunch of values at once, which are then written to an internal list referred to as the store. read_store operations then extract the desired data from this store instead of from the instrument itself. Because accessing the store takes considerably less time than communicating with an external instrument, this saves a lot of time.

write_action operations are used by the autoprofile system to perform actions on the system using a write command. This is accomplished using a dictionary of available action operations indexed by string. This string is set by the autoprofile, and the corresponding action operation is performed. Because write_action operations are write operations, they can have associated check_set and check_actual values. If they do, their keys will most likely be determined by the values produced by these check operations.

## Transducer files
Transducer files are special instrument files that contain information on a specific transducer. A read operation can point to a transducer file instead of including certain information. The details from the transducer are appended to the sensor file so that the correct information is provided. A transducer file includes the following, each corresponding to the appropriate detail that would normally be in the operation:
* t_name
* t_id
* details
* transform_eq
* check_date
* cal_date
* check_freq
* cal_freq
* rep_num
* uncertainty

## PID instruments
PID instruments are special virtual instruments that make use of the PID driver. These virtual instruments allow for PID control of an output control variable with respect to the value of an input measure. The following additional details are required for a PID instrument file:
* "measure" (LIST of (STRING, STRING); The measurement that controls the PID. The first string is the measurement instrument's instrument file, while the second string is the read operation that reads the measure.)
* "control" (LIST of (STRING, STRING); The control variable. The first string is the controlled instrument's instrument file, while the second string is the write operation that sets the control.)
* "Proportional" (FLOAT; The proportional gain of the PID. This should be set first, to about a quarter of the value that causes the system to oscillate.)
* "Integral" (FLOAT; The integral gain of the PID. This should be set second (start from 0) and should be increased until the system settles to the desired value in reasonable time without getting unstable.)
* "Derivative" (FLOAT; The derivative gain of the PID. This should be set last (start from 0) and should be increased until the system settles quickly without overshoot.)
* "positive_feedback" (BOOLEAN; Controls whether the feedback is positive or negative. Positive feedback is the default, and is used for systems whose measure value is monotonically non-decreasing with respect to the control variable. Negative feedback should be used in cases where the measure value is monotonically non-increasing with respect to the control variable. If the two are not monotonically linked, a PID should not be used, as the control system can get trapped in local minima or maxima and fail to control properly.)
* "max" (FLOAT; The maximum allowed value for the control variable. Used to prevent a system running away if something goes wrong.)
* "min" (FLOAT; The minimum allowed value for the control variable. Used to prevent a system running away if something goes wrong.)

***

# Job Files
Job files consist of a dictionary containing at least the following details:
* job_name (STRING; The name the logger uses to refer to this job.)
* out_dir (STRING; The local directory that this job will write to. Normally an address in I:\\.)
* filename (STRING; the name that this job will be saved under. The files will be saved in a folder with the date, time, and filename, containing data, points, and source files for both raw and transformed data, as well as the sensor file.)
* min_interval (INTEGER; The minimum number of minutes allowed between cycles. Can be 0.)
* time (INTEGER; Starting time. Normally 0.)
* instruments (DICTIONARY of (STRING: STRING); The instrument files that need to be used. The key of each entry should be the instrument_id of that instrument, while the data should be the filename of that instrument file including any path information required.)
* logged_operations (LIST of (STRING); The read operations that need to be used. Each should take the form of {instrument}.{operation}, where {instrument} is the instrument_id of the instrument being read and {operation} is the id of the read operation being performed.)
* details (DICTIONARY of (STRING: DICTIONARY of (STRING: STRING)); Additional details regarding instrument positions and other notable information. The outer-most dictionary uses instruments as keys, while the inner-most dictionaries use operations as keys. Only notable keys need to be filled in.)
* references (DICTIONARY of (STRING: DICTIONARY of (STRING: VARIOUS)); Contains the reference "operations" that the logger will record. These operate as phantom instruments that can be graphed or logged from the instrument "reference.[REFERENCE_NAME]". The outer-most dictionary uses the keys provided as the operations' names, while the inner-most dictionaries each include eight specific details which define the reference. References are explained in further detail below.)
* graphs (DICTIONARY of (STRING: DICTIONARY of (STRING: STRING, STRING: DICTIONARY of (STRING: STRING))); Contains the graphs that should be automatically generated on starting the job. The outer-most dictionary uses the keys provided as the graph names, the middle dictionaries contain the x-axis for each graph, and the inner-most dictionaries contain the y-axes for each graph.)

## References
The logger can use plot and log special simulated instruments, called references. These take information from other instruments in the job and perform mathematical operations on it to present it in a way that might make things more clear. There are two main types of references: humidity references, and math references.

### Humidity References
Humidity references call on the refcalc.py script to perform conversions between different humidity values. They take an initial reference humidity "hum" as well as pressure "p1", temperature "t1" and dew/frost state "df1" at this humidity, and then calculate the humidity at another point with pressure "p2", temperature "t2" and dew/frost state "df2", using an equation defined by "type". "hum", "p1", "p2", "t1", and "t2" are all STRINGS of the same form as detailed in logger_operations, indicating which operation defines their values. "df1" and "df2" are INTEGERS, with 0 being dew and 1 being frost. "type" is a STRING consisting of the type of humidity measurement being made and the type of humidity measurement being calculated. d represents a dew point, and h represents a relative humidity. The first letter in the string is what is being calculated, and the second letter is what is being provided. For instance, calculating a dew point from a relative humidity would have "type": "dh".

### Math References
Math references use simple equations to calculate a relationship between two values. They do not use "hum", "p1", or "p2". "t1", and "t2" are both STRINGS of the same form as detailed in logger_operations, indicating the two operations whose relationship is being described. "df1" and "df2" are FLOATS, used to describe their relationship. "type" is a STRING, either "ms" or "mm". "ms" is the math-sum operation, and will calculate "t1.df1+d2.df2". "mp" is the math-product operation, and will calculate "t1^df1.t2^df2". By changing the values of df1 and df2, more complicated equations than simple sums or products can be produced. Some examples include:
* type = "ms", df1 = 2, df2 = 0, Result is twice t1, with no t2 present.
* type = "ms", df1 = 1, df2 = -1, Result is the difference between t1 and t2.
* type = "ms", df1 = 0.5, df2 = 0.5, Result is the average of t1 and t2.
* type = "mp", df1 = 2, df2 = 0, Result is the square of t1, with no t2 present.
* type = "mp", df1 = 1, df2 = -1, Result is the ratio of t1 to t2.
* type = "mp", df1 = 0.5, df2 = 0.5, Result is the multiplicative average of t1 and t2.

***

# Autoprofile Files
Autoprofile files consist of comma delineated lines containing the following:
* filename (Must start with an "a". Suggested name is "a{start date}\_{client company name}\_{name of DUT}")
* write operation names (First three must be "Points", "Soak", and "Assured". Names are recommended to indicate both the instrument and operation being used in the write command.)
* write operation ids (First three should be left as "". Additional operations should take the form of {instrument}.{operation}, where {instrument} is the instrument_id of the instrument being written to and {operation} is the id of the write operation being performed.)
* values to write (An individual line is detailed below.)

Values should be as follows:
* Points (The number associated with this point. The first one should be "1", second "2", and so on.)
* Soak (The time, in minutes, that the logger should wait before trying to move to the next point. If Assured isn't set, this will be approximately how long the logger waits between points. If Assured is set, this will be how long the logger waits before checking Assured.)
* Assured (The operation that Assured is trying to wait for. "0" or less is no Assured, "1" is the first instrument operation, "2" is the second, and so on. Only one value can be assured against at a time.)
* additional operations (The value that will be written to the instrument using this write command.)

No additional lines should be included after the last comma delineated line, nor should any additional commas be included at the end of lines 2 and onwards. Line 1, because it only contains the filename, can contain any number of superfluous characters after the first comma.

***

# The Control Window
This is the window that opens when you start the program by running the main_controller.py script.

### Open Job
This button allows you to open a job and all instruments required for that job. It defaults to opening from the job_files folder.

### Open Instrument
This button allows you to open an instrument. It defaults to opening from the instruments folder.

### Jobs
This is a list of the currently open jobs. Double-clicking one will open the Job Window for that specific job.

### Instruments
This is a list of the currently open instruments. Double-clicking one will open the Instrument Window for that specific instrument.

***

# The Job Window
The Job window is the main window used when running this software. There is a lot to consider here, so it will be discussed sequentially.

## GRAPH
This menu contains options related to the graph tabs.

### Add Graph
This creates a new graph tab. It takes three arguments:

* Name (The title shown on the tab. Should be descriptive of what is depicted. If a graph with the same name [NAME] already exists, the new graph will be named [NAME]' instead.)
* X Axis (The x-axis of the graph. For reasons of clarity, only one x-axis is allowed per graph.)
* Y Axis (The trace of the graph. Additional traces can be added using the "Append Graph" option in the dropdown menu.)

### Append Graph
This will add a trace to an already existing graph. It takes two arguments:

* Append Graph (This is the graph that will be appended. The list contains all the currently existing graphs.)
* New Y Axis (This is the trace that should be appended. If that trace is already on that graph, this does nothing.)

### Detract Graph
This will remove a trace from an existing graph. It takes two arguments, one after the other:

* Choose Graph (This is the graph that will be detracted. The list contains all the currently existing graphs.)
* Choose Axis (This is the trace to be removed. The list contains all traces on the graph chosen above.)

### Remove Graph
This will remove a graph from the graph list. It takes one argument:

* Remove Graph (This is the graph to be removed. The list contains all the currently existing graphs.)

## CONTROL SIDEBAR
This sidebar contains the overriding control buttons for the job, as well as some information considered useful for all tabs to have access to.

### Start, Pause, and Resume buttons
These three buttons control the process of logging. Start will begin the logging function, pause will temporarily halt it, and resume will undo pausing.

### Numbers
Two numbers sit between the Resume button and the Reading line, though normally only one of them is visible. The number on the left is the total number of cycles the logger has gone through. The number on the right will only appear when using the "Next N" function, and will show the number of cycles left before the function has finished.

### Reading:
This line lists what is currently being read in the form of {instrument}.{operation}. If the cycle has finished reading the instruments, this will instead say "waiting..."

### Next Point In:
This line estimates how long it will be before the next point is taken. The time is approximate, based on how long the cycles have previously taken. If it says "now", the logger is currently moving to the next point. If assured is being used, this line may inform when time is up but the controlled variable is not at it's desired value. This is expressed by "When" and the condition it is looking to correct.

## LOG TAB
This tab contains a written log of each cycle as it's recorded. It can be hard to read, especially if the logger is still running, but it can be useful for bug-fixing if something goes wrong.

## POINTS TAB
This tab contains the current information on the calibration, as well as some additional controls for recording data in the points files.

### Central Table
This table lists the operations being logged, as well as the last logged values, means, and standard deviations of each of them. If one or more numbers are return as "nan", then something is going wrong with the reading of that value. For instance, the Thunder Scientific 2900 Humidity Generator will return "nan" when reading its relative humidity value while it's not running.

### Last N and Next N
These two buttons will each force the logger to record a point. Last N will calculate the point with respect to the last N cycles, while Next N will run for N cycles and then record the point. In either case, N is controlled by the box below the two buttons.

### Transformed
This toggle changes whether the values displayed in the table are raw values or transformed. It defaults to on. Note that regardless of its value, the graphs will display transformed data, never raw.

### Comment
When a point is taken, if there is a comment in this box, it will be recorded with that point and then the box is cleared.

## PROFILE TAB
This tab is used to read and change the autoprofile that controls the job. If the job is controlled manually, this tab can be ignored.

### Table
This table shows the current autoprofile, as detailed in the Autoprofile Files chapter. Note that the program will crash if certain values are left blank (such as Soak and Assured) but can handle empty cells in the additional columns.

### Next Point and Move to Selected
These two buttons allow the current point to be moved. Next point will ignore Soak and Assured settings and immediately record the point before moving to the next one. Pressing Move to Selected while a row is highlighted (by pressing the number left of the Point column) will move the setpoints to those values, but will not save the current point.

### Load File
This button allows you to open autoprofile files. It defaults to opening from the autoprofiles folder.

### New Set and New Point
These two buttons allow you to manually modify the autoprofile. New Set creates a new column, and asks for three inputs: "Name", the name of the column; "Instrument", the instrument that will be set; and "Set" the write operation to be performed on said instrument. New point creates a new row, which is completely blank.

### Error and STDev values
These two input boxes define the precision desired for the Assured function. Error defines how close to the set value the program is willing to accept, and STDev defines how stable a response the program is willing to accept. Unfortunately, due to a bug, the labels for these boxes are currently invisible.

## GRAPH TABS
Each of these tabs contains one graph. These graphs automatically update when new data is recorded or when the traces are changed. The buttons available at the bottom of the graphs are automatically put their by the plugin, but should operate as desired. The traces show the transformed data of each operation listed in the legend.

***

# The Instrument Window
The instrument window is used for checking the function of new instruments, as well as reading or writing to specific instruments for checking or control purposes.

### Read
Contains a list of read commands from the instrument's operations list. The box in the middle will be filled with what is read when you press the Read button.

### Write
Contains a list of write commands from the instrument's operations list. The box in the middle will be written to the instrument with that command when you press the Write button.

### Action
Contains a list of action commands from the instrument's operations list. Pressing the Action button will perform the selected action.