try:
    from datetime import datetime
    import os
    from dateutil.relativedelta import relativedelta
except:
    print ("Please verify that you have installed the following libraries: \ndatetime\nos\ndateutil")
    os._exit(0) #stops program
#Function to append to a file with a new string
def writeToTxt(file, string):
    text_file = open(file, "a")
    text_file.write(string)
    text_file.close()

#Function to overwrite a file with a new string
def overwriteTxt(file, string):
    text_file = open(file, "w+")
    text_file.write(string)
    text_file.close()

#Replace a string in a file with a new one
def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            #print '"{old_string}" not found in {filename}.'.format(**locals())
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        #print 'Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals())
        s = s.replace(old_string, new_string)
        f.write(s)

#Get today's date
today = str(datetime.now()).split(" ")[0]
print ("Today's date: " + today)

#Check if folders (where the CSVs will be stored) exist, if not, create them
if not(os.path.isdir("reports/")):
    os.makedirs("reports/")
    print ("Creating folder 'reports'...")
if not(os.path.isdir("data/")):
    os.makedirs("data/")
    print ("Creating folder 'data'...")

#Present the different modes and ask the user to choose the desired
print ("Enter the mode")
print ("1: Check-in employees")
print ("2: Check-out employees")
print ("3: Generate report")
mode = input("Enter the mode: ") #String

print (mode)



shouldExit = False
if mode == "1":
    while not shouldExit:
        #ask for employee number
        employeeNumber = input("Enter the employee number to check-in or '0' to exit: ")
        if employeeNumber == "0":
            shouldExit = True
            break
        #get the current time to assign to employee sign in time
        time_mins = datetime.now().strftime('%H:%M')
        print (employeeNumber, time_mins)
        #write the employees number with its time of arrival on the data csv
        writeToTxt("data/" + today + ".csv", employeeNumber + "," + time_mins + "\n")

if mode == "2":
    while not shouldExit:
        #ask for employee number
        employeeNumber = input("Enter the employee number to check-out or '0' to exit: ")
        if employeeNumber == "0":
            shouldExit = True
            break
        time_mins = datetime.now().strftime('%H:%M')
        print (employeeNumber, time_mins)
        with open("data/" + today + ".csv") as f:
            lines = f.readlines()

        employee_lineIndex = 0
        for i in lines:
            if i.split(",")[0] == employeeNumber:
                break
            employee_lineIndex = employee_lineIndex + 1

        #replace the previous data file with the new one which includes the time of sign-out
        try:
            inplace_change("data/" + today + ".csv", lines[employee_lineIndex], lines[employee_lineIndex].replace("\n", "") + "," + time_mins + "\n")
        except:
            print ("Error, that user has not signed in!")

if mode == "3":
    ###Copy file's data to "" + today + ".csv"
    with open("data/" + today + ".csv") as f:
        s = f.read()
    with open("reports/" + today + ".csv", 'w+') as f:
        f.write(s)
    ###


    with open("data/" + today + ".csv") as f:
        lines = f.readlines()

        for line in lines:
            splitted_line = line.split(",")
            print (splitted_line)
            #calculate the difference in hours
            start = datetime.strptime(splitted_line[1], '%H:%M')
            ends = datetime.strptime(splitted_line[2].replace("\r", "").replace("\n", "") , '%H:%M')
            diff = relativedelta(ends, start)
            print ("Hours worked: ", diff.hours)
            print ("Minutes worked: ", diff.minutes)
            #calculate the money gained
            moneyGained = str(round(diff.hours * (7.25), 2) + round(diff.minutes * (7.25/60.0), 2))
            print ("Money gained: ", moneyGained)
            inplace_change("reports/" + today + ".csv", line, line.replace("\n", "").replace("\r", "") + ",$" + moneyGained + "\n")

        #add a headline to the excel
        with open("reports/" + today + ".csv") as f:
            s = f.read()

        with open("reports/" + today + ".csv", 'w+') as f:
            s = s.replace(s, "EMPLOYEE ID,START HOUR,EXIT HOUR,MONEY GAINED\n" + s)
            f.write(s)
