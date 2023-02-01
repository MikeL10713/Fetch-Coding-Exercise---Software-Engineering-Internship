import csv, sys

# store the second argument as the points to spend (first argument is points_spending.py)
pointsToSpend = int(sys.argv[1])

# read in csv data and store each line for later use
data = []
with open("transactions.csv", mode ="r") as file:
  for line in csv.reader(file):
    data.append(line)
# header line not needed, so we remove it
data = data[1:]

# create a dict to store the point balances for each payer and go through the data to update point balances
pointBalances = {}
for line in data:
  pointBalances[line[0]] = pointBalances.get(line[0], 0) + int(line[1])

# in order to make comparing dates easier, replace the time section of the data with a 
#   tuple containing number of days since the year 0 and number of seconds since the start of that day
for line in data:
  dateAndTime = line[2].split("T")
  dateParts = dateAndTime[0].split("-")
  timeParts = dateAndTime[1][:-1].split(":")
  line[2] = (int(dateParts[0]) * 365 + int(dateParts[1]) * 31 + int(dateParts[2]), int(timeParts[0]) * 3600 + 
    int(timeParts[1]) * 60 + int(timeParts[2]))

# sort the data by time first and then date to get relative position correct for same dates
data.sort(key = lambda d : d[2][1])
data.sort(key = lambda d : d[2][0])

# go through the transactions and spend points, making sure to prevent negative balances
for transaction in data:
  payer = transaction[0]
  availablePoints = int(transaction[1])
  # if more points are available then needed to spend requested amount, subtract just what is needed and 
  #   break to return remaining balances 
  if availablePoints > pointsToSpend:
    pointBalances[payer] -= pointsToSpend
    break
  else:
    pointBalances[payer] -= availablePoints
    pointsToSpend -= availablePoints
    if pointsToSpend == 0:
      break
    
# output of point balances after spending
print(pointBalances)
  

