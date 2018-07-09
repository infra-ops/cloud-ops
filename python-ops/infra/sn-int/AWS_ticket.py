import boto3
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import threading

class create_aws_case():
    def __init__(self):

        self.client = boto3.client('support',region_name='us-east-1',aws_access_key_id='AKIAJ3K3EUMCD7SHJDFA',aws_secret_access_key='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')
        self.serviceList = self.client.describe_services()
        self.severityList = self.client.describe_severity_levels()
        # thread = threading.Thread(target=lambda: self.guiImplementation())
        # thread.start()
        self.guiImplementation()

    def getServiceList(self):
        serviceList = []
        for line in self.serviceList['services']:
            serviceList.append(line['name'])
        print("service list received")
        serviceList.sort()
        return serviceList

    def getSeverityList(self):
        severityList = []
        for line in self.severityList['severityLevels']:
            severityList.append(line['name'])
        print("severity list received")
        return severityList

    def getCategoryList(self,Service):
        categoryList = []
        for line in self.serviceList['services']:
            if(line['name'] == Service):
                for row in line['categories']:
                    categoryList.append(row['name'])
                return categoryList

    def getServiceCode(self,serviceName):
        for line in self.serviceList['services']:
            if(line['name'] == serviceName):
                return line['code']

    def getSeverityCode(self, severityName):
        for line in self.severityList['severityLevels']:
            if(line['name'] == severityName):
                return line['code']

    def getCategoryCode(self,serviceName, categoryName):
        for line in self.serviceList['services']:
            if(line['name'] == serviceName):
                for row in line['categories']:
                    if(row['name'] == categoryName):
                        return row['code']

    def createCase(self,event):

        subject = self.entrySubject.get()
        communicationBody = self.entryBodyLabel.get(1.0,END)
        language = 'en',
        serviceCode = self.getServiceCode(self.comboStateService.get())
        categoryCode = self.getCategoryCode(self.comboStateService.get(), self.comboStateCategory.get()),
        severityCode = self.getSeverityCode(self.comboStateSeverity.get())

        self.response = self.client.create_case(
            subject=self.entrySubject.get(),
            communicationBody=self.entryBodyLabel.get(1.0,END),
            language='en',
            serviceCode=self.getServiceCode(self.comboStateService.get()),
            categoryCode=self.getCategoryCode(self.comboStateService.get(),self.comboStateCategory.get()),
            severityCode=self.getSeverityCode(self.comboStateSeverity.get())
        )

        print(self.response['caseId'])

    def spawnThread(self):
        print("Thread Spawned")
        self.selectCategory = ttk.Combobox(self.root, textvariable=self.comboStateCategory,values=self.getCategoryList(self.selectService.get()),width=26)


    def guiImplementation(self):
        self.root = Tk()
        s = ttk.Style()
        s.theme_use('clam')
        self.root.geometry("350x500")


        self.subjectLabel = Label(self.root, text="Subject")
        self.entrySubject = Entry(self.root,width = 40)
        self.subjectLabel.grid(row=0, column=0, pady=10, padx=10)
        self.entrySubject.grid(row=0, column=1, pady=10, padx=10)

        self.bodyLabel = Label(self.root, text="Body")
        self.entryBodyLabel = Text(self.root,width = 30, height = 5)
        self.bodyLabel.grid(row=1, column=0, pady=10, padx=10)
        self.entryBodyLabel.grid(row=1, column=1, pady=10, padx=10)

        self.comboStateService = StringVar(self.root)
        self.comboStateService.set("Certificate Manager")

        self.selectServiceLabel = Label(self.root, text="Service")
        self.selectService = ttk.Combobox(self.root, textvariable=self.comboStateService,values=self.getServiceList(),width=26)
        self.selectServiceLabel.grid(row=2, column=0, pady=10, padx=10)
        self.selectService.grid(row=2, column=1, pady=10, padx=10)

        self.comboStateCategory = StringVar(self.root)
        # self.comboState.set("RUN")

        self.selectCategoryLabel = Label(self.root, text="Category")
        self.selectCategory = ttk.Combobox(self.root, textvariable=self.comboStateCategory,values=self.getCategoryList(self.selectService.get()),width=26)
        # self.entrySelectCategory = Entry(self.root, width = 40)
        self.selectCategoryLabel.grid(row=3, column=0, pady=10, padx=10)
        # self.entrySelectCategory.grid(row=3, column=1, pady=10, padx=10)
        self.selectCategory.grid(row=3, column=1, pady=10, padx=10)
        # print("service is "+self.selectService.get())


        self.comboStateSeverity = StringVar(self.root)
        # self.comboState.set("RUN")

        self.selectSeverityLabel = Label(self.root, text="Severity")
        self.selectSeverity = ttk.Combobox(self.root, textvariable=self.comboStateSeverity,values=self.getSeverityList(),width=26)
        self.selectSeverityLabel.grid(row=4, column=0, pady=10, padx=10)
        self.selectSeverity.grid(row=4, column=1, pady=10, padx=10)

        self.go_but = Button(self.root, text="Create Ticket")
        self.go_but.grid(row=5, columnspan=2, pady=5)

        def selectCat(event):
            print(self.getCategoryList(self.selectService.get()))
            self.selectCategory['values'] = self.getCategoryList(self.selectService.get())
            print("select cat activated")
        self.selectCategory.bind("<Button-1>",selectCat)

        self.go_but.bind("<Button-1>", self.createCase)

        self.root.mainloop()

createCase = create_aws_case()
# createCase.getSeverityList()
