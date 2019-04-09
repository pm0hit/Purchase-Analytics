import re
import os

class Department_Data:
    numberOfOrders=1;
    numberOfFirstOrders=0;
    percentage=0.0

    def __init__(self,departmentId=None):
        self.departmentId=departmentId

    #To calculate no of orders
    def addOrder(self):
        self.numberOfOrders=self.numberOfOrders+1

    #To calculate no of first orders
    def addFirstOrder(self):
        self.numberOfFirstOrders=self.numberOfFirstOrders+1

    #to print the data and send it to the report
    def getPrintData(self):
        return str(self.departmentId)+", "+str(self.numberOfOrders)+", "+str(self.numberOfFirstOrders)+", "+str(self.getPercentage())

    def getPercentage(self):
        return round(self.numberOfFirstOrders/self.numberOfOrders,2)

#To register products
class Products:
    def __init__(self, productId=None,productName=None,aisleId=None,departmentId=None):
        self.productId=productId
        self.productName = productName
        self.aisleId = aisleId
        self.departmentId = departmentId

#Convert a string into array seprating with comma 
#ignoring the comma within the inverted comma
#param 1 : x : string of any kind
#return array of string
def csvLineToArray(x):
    x=str(x)
    line=[]
    regex = r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)"
    matches = re.finditer(regex, x, re.MULTILINE)
    startPoint=0
    for matchNum, match in enumerate(matches, start=1):
        line.append(x[startPoint:match.start()])
        startPoint=match.end()
    line.append(x[startPoint:len(x)-1])
    return line

#Main Program
product_list={}
deptList={}
iteration=0
direct = ''
productFileName=''
orderFileName=''

print("1. Run with original (/input) data.")
print("2. Run with test1 (/insight_testsuite/tests/test1/input) data.")
print("3. Run with your-own-test_1 (/insight_testsuite/tests/your-own-test_1/input)  data.")
runType=int(input("Select the input data folder : "))

if runType==1:
    print('in 1')
    direct = './input/'
    productFileName='products.csv'
    orderFileName='order_products.csv'
elif runType==2:
    direct = './tests/test_1/input/'
    productFileName='products.csv'
    orderFileName='order_products.csv'
elif runType==3:
    direct = './tests/your-own-test_1/input/'
    productFileName='products.csv'
    orderFileName='order_products_test.csv'

f = open(direct+productFileName, 'r',encoding='utf8', errors='ignore')

f.readline()
for x in f:
    iteration=iteration+1
    x=csvLineToArray(x)
    x[0]=int(x[0])
    x[2]=int(x[2])
    x[3]=int(x[3])

    try:
    	deptList[x[3]].addOrder()
    except KeyError:
    	deptList[x[3]]=Department_Data(x[3])

    product_list[x[0]]=Products(x[0],x[1],x[2],x[3])
f.close()

itr=0
f = open(direct+orderFileName, 'r',encoding='utf8', errors='ignore')
f.readline()
for x in f:
    itr=itr+1
    x=csvLineToArray(x)
    x[1]=int(x[1])
    x[3]=int(x[3])
    if x[3]==0:
        deptList[product_list[x[1]].departmentId].addFirstOrder()
f.close()

keyList=list(deptList.keys())
list.sort(keyList)

f = open(direct+"../output/report.csv", 'w+',encoding='utf8', errors='ignore')
f.write('department_id,number_of_orders,number_of_first_orders,percentage\n')
for x in keyList:
    f.write(deptList[x].getPrintData()+'\n');
f.close();
print("Done exporting.")
name = input("")