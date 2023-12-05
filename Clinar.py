"""
Name: Amanda Fuenzalida (AIF), Tim Anastacio (TJA),Selina Qian (JQ), Kimberley Muchenje (KTM), Oliver Tipton (OPT), Imer Ramadanovic (IHR)

Final Project

"""




import tkinter as tk
from tkinter import ttk 
from tabulate import tabulate

class Genes:

  def __init__(self, master):
    
    """
    Author: AIF, TJA, OPT, JQ

    Section for GUI command: Creates the graphic to present all our information on. Runs the functions connected to the dropdown menus, buttons, as well as entry boxes. 

    Arguments: Self (define the attributes of the class) and Master (knows to project information and widgets)

    Returns: The presented interactive graphic for the user to select and enter wanted information. Selecting a specific option will return either presented or calculate information back to the user.
    """

    self.master = master
    self.master.geometry('700x400')
    self.master.configure(bg='light blue')
    #KTM -change background color of window 

    self.gene_dict = file_parser('tester.txt')
    #TJA - sets the method of gene dict to the dictionary created using the file parser function
    
    
    self.main_label = tk.Label(self.master, text = 'Welcome to ClinVar!')
    self.main_label.grid (row = 1, column = 5)
    #TJA - Takes a greeting message and outputs it onto the GUI at row position 1, column position 5

    self.info_label = tk.Label(self.master, text = 'For overall summaries of human gene variants, select one of these options:')
    self.info_label.grid (row = 2, column = 5)
    #TJA - Gives the user an informative description of what to do with the explore ClinVar drop-down menu and Get Stats button


    self.entry_label = tk.Label(self.master, text = 'To get specific info about a gene, enter a gene name: ')
    self.entry_label.grid (row = 8, column = 5)
    #TJA - Gives the user an informative description of what to do with the Entry box for a specific gene name, the Select an option drop-down menu, and Enter button

    self.entry_name = tk.Entry(self.master)
    self.entry_name.grid (row = 9, column = 5)
    #TJA - Creates an entry box for the user to input a specific gene name as a string

    self.gene_display = ''
    self.gene_display_text = tk.StringVar()
    self.gene_display_text.set(self.gene_display)
    self.gene_display_label = tk.Label(master, textvariable = self.gene_display_text)
    self.gene_display_label.grid(row = 6, column = 5)
    # IHR - lines 43-47 are meant to provide the text with a blank string so that new entries aren't printed on top of old outputs

    self.gene_display_2 = ''
    self.gene_display_text_2 = tk.StringVar()
    self.gene_display_text_2.set(self.gene_display)
    self.gene_display_label_2 = tk.Label(master, textvariable = self.gene_display_text)
    self.gene_display_label_2.grid(row = 13, column = 5)
    # IHR - lines 50-54 are meant to provide the text with a blank string for the second gene so that new entries aren't printed on top of old inputs
    
    options = ['All', 'Total Submissions', 'Total Alleles', 'Reported Submissions','Pathogenic Alleles', 'Likely Pathogenic Alleles', 'Mim Number', 'Uncertain Number', 'Number With Conflicts'] #AIF, OPT creates the options seen in the second dropdown menu
    self.value_in = tk.StringVar(self.master) #AIF, OPT - to start the dropdown menu, you have define Master under this class from Tkinter
    self.value_in.set('Select an option') #AIF, OPT - What is first displayed to the user to click on the dropdown menu
    self.question_menu = tk.OptionMenu(self.master, self.value_in, *options) #AIF - Use of another Tkinter class to define our list 'options' as a dropdown menu and so the values can be selected with a return. 
    self.question_menu.grid(row = 11, column = 5)#AIF, OPT - Sets the placement of the dropdown menu
    
    self.name_button = tk.Button(self.master, text = 'Enter', command = lambda:gene_finder(self,self.entry_name.get(), self.value_in.get())) #AIF, OPT - What causes the selected option from the dropdown menu to run once the user has chosen one
    self.name_button.grid (row = 12, column = 5)
    #TJA - Establishes a button to take the information from the gene name entry box and the Select an option drop-down menu that will take this user-inputted information into the corresponding gene_finder function

    
    self.values = get_values(self.gene_dict)
    #OPT, AIF - sets the self values by running the gene dictionary as an argument through the get_values function

    self.total_var = get_all_variants(self.values)
    #OPT, AIF - sets the total variants by running the self values created above as an argument through the get_all_variants function
    
    self.total_path_var = pathogenic_vars(self.values)
    #OPT, AIF - sets the total pathogenic variants by running the self values through the pathogenic_vars funciton
    
    self.total_unsig = uncertain_sig_vars(self.values)
    #OPT, AIF - sets the total variants with uncertain significance by running self valuess through the uncertain_sig_vars function

    self.avg_var = average_vars(self.values)
    #OPT, AIF - sets the average variants by running the self values through the average_vars function
    
    self.all_stats = getall_stats(self.values)
    #OPT, AIF - sets all statics by running the self values through the getall_stats function

    self.stats_table = create_table(self.all_stats)
    #OPT, AIF - creates a stats table by running all of the statistics through the create_table function

    general_options = ['Total Variants', 'Total Pathogenic Variants', 'Variants with Uncertain Significance', 'Average Variants per Gene', 'All Statistics']
    #OPT, AIF - lists all of the options for the dropdown 
    self.value_in_gen = tk.StringVar(self.master)
    #OPT, AIF - uses StringVar as the class from tkinter for starting the dropdown
    self.value_in_gen.set('Explore ClinVar Data')
    #OPT, AIF - sets the label for the front of the dropdown list 
    self.question_menu2 = tk.OptionMenu(self.master, self.value_in_gen, *general_options)
    #OPT, AIF - creates the dropdown menu using the OptionMenu tk widget
    #OPT, AIF - uses the self master, the StringVar widget from tkinter, and our list of options for the dropdown
    self.question_menu2.grid(row = 4, column = 5)

    self.info_button = tk.Button(self.master, text = 'Get Stats', command = lambda:get_stats(self,self.value_in_gen.get()))
    #OPT, AIF - For the first dropdown menu, this connects for the function connected to a selected option to be run once the user clicks in the "action" button of get stats
    self.info_button.grid (row = 5, column = 5) #OPT, AIF - sets the placement of the 'Get Stats' button


    
    self.main_label = tk.Label(self.master, text = "Enter two genes to compare") #JQ - the GUI prompts the user to compare two genes with each other
    self.main_label.grid(row = 14, column = 5) #JQ - locate the label in the master
    self.left_label = tk.Label(self.master, text = "First Gene")#JQ - the GUI prompts the user to enter the first gene
    self.left_label.grid(row = 15, column = 4) #JQ - locate the label in the master
    self.right_label = tk.Label(self.master, text = "Second Gene") #JQ the GUI prompts the user to enter the second gene
    self.right_label.grid(row = 16, column = 4) #JQ - locate the label in the master
    self.entry1 = tk.Entry(self.master) #JQ - the entry box for the first gene
    self.entry1.grid(row = 15, column = 5) #JQ - locate the enter box in the master
    self.entry2 = tk.Entry(self.master) #JQ - the entry box for the second gene
    self.entry2.grid(row = 16, column = 5) #JQ - locate the enter box is the master
    
    self.button = ttk.Button(self.master, text = "Compare", command = lambda:compare_gene(self, self.entry1.get(),self.entry2.get())) #JQ - the button to run the comomapre gene function
    self.button.grid(row = 19, column = 5) #JQ - locate the output in the master
    
  

    """
    section for functions
    """

    def compare_gene(self, left_gene, right_gene):
      """
      Author: JQ, KTM 
      This function takes in two entry input from the user and call the file_parser function to output the desired tow list of information
      """

      data_left = self.gene_dict.get(left_gene)
      data_right = self.gene_dict.get(right_gene)
      #JQ, KTM - select the statistics for two genes entered by the user in entry boxes 
      header = ["Total\nSubmissions", "Total\nAlleles",	"Reported\nSubmissions",	"Pathogenic\nAlleles",	"MIM\nNumber",	"Uncertain\nNumber",	"Number with\nConflicts"]
      #JQ, KTM - makes a list of headers for the table 
      table2 = [data_left,data_right]
      #JQ, KTM - make a 2d list of the summary stats for 2 genes 
      mytable2 = tabulate(table2, headers=header, tablefmt= "simple")
      #JQ, KTM - call the tabulate function to transform the 2d list into a table-formatted sting
      test_table = tk.Label(self.master, text = mytable2)
      test_table.grid (row = 40, column = 5) #JQ, KTM - locate the table in the center of the master



      
    


    def gene_finder(self, gene_name, *args):
      '''
      Author: TJA, OPT, AIF, IHR
      Takes in user-inputted strings of gene name and desired information. Uses the gene_dict dictionary to return the desired information.

      Arguments:
      self
      gene_name = string of the gene name inputted from the entry box
      *args = desired information taken from a dropdown menu

      Returns:
      Returns a string with the desired information corresponding with the inputted gene name and is printed onto the GUI.

      '''
      
      column = self.value_in.get()
      #TJA, OPT - sets column variable equal to the value of the dropdown list that the user selected
      #OPT - helps run through the drop down list using the *args argument 
      
      info = self.gene_dict[gene_name]
      #TJA, OPT - uses the gene dictionary from the file_parser function and uses the user-inputted gene name as the key. Sets variable info to the associated value pair.


      if column == 'All':
        #TJA - if user wants all associated gene information, will run this if statement
        for i in range(0, len(info)):
          
          if info[i] == '-':
          
            info[i] = 0
          #TJA - if there is a - in index position i of the info list, will replace the - with a 0.

        
        result = tk.Label(self.master, text = info)
        # IHR - sets result variable so that it is not writing over a previous output & supplies text for the output
        
        result.grid(row = 13, column = 5)
        #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
      
      elif column == 'Total Submissions':
        #TJA - will run this if statement user selected Total Submission
        
        if info[0] == '-':
        
          result = tk.Label(self.master, text = 'The total submissions for this gene is 0.')
          # IHR - sets result variable so that it is not writing over a previous output & supplies additional text for the output
          
        
          result.grid(row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
        
        else:

          result = tk.Label(self.master, text = 'The total submissions for this gene are ' + info[0])
          # IHR - sets result variable so that it is not writing over a previous output & supplies additional text for the output

          result.grid(row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
      
      elif column == 'Total Alleles':
        #TJA - will run this if statement if user selected Total Alleles
        
        if info[1] == '-':
          
          result = tk.Label(self.master, text = 'The total alleles for this gene is 0.')
          # IHR - sets result variable so that it is not writing over a previous output & supplies additional text for the output

          result.grid(row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
        
        else:
        
          result = tk.Label(self.master, text = 'The total alleles for this gene are ' + info[1])
          # IHR - sets result variable so that it is not writing over a previous output & supplies additional text for the output

          result.grid(row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.

      
      elif column == 'Reported Submissions':
        #TJA - will run this if statement if user selected Reported Submissions
        
        if info[2] == '-':
        
          result = tk.Label(self.master, text = 'The total reported submissions for this gene are 0.')
          # IHR - sets result variable so that it is not writing over a previous output & supplies additional text for the output

          result.grid(row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
        
        else:
        
          result = tk.Label(self.master, text = 'The total reported submissions for this gene are ' + info[2])
          # IHR - sets result variable so that it is not writing over a previous output & supplies additional text for the output

          result.grid(row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
    
      elif column == 'Pathogenic Alleles':
        
        if info[3] == '-':
        
          result = tk.Label(self.master, text = 'The total number of pathogenic alleles for this gene is 0.')
          # IHR - sets result variable so that it is not writing over a previous output & supplies text for the output

          result.grid(row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
        
        else:
        
          result = tk.Label(self.master, text = 'The total number of pathogenic alleles for this gene are ' + info[3])
          # IHR - sets result variable so that it is not writing over a previous output & supplies additional text for the output

          result.grid(row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
      
      elif column == 'Likely Pathogenic Alleles':
        #TJA - will run this if statement if user selected Likely Pathogenic Alleles
        
        if info[4] == '-':
        
            result = tk.Label(self.master, text = 'The total number of likely pathogenic alleles for this gene is 0.')
            # IHR - sets result variable so that it is not writing over a previous output & supplies text for the output

            result.grid(row = 13, column = 5)
            #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
        
        else:
        
          result = tk.Label(self.master, text = 'The total number of likely pathogenic alleles for this gene are ' + info[4])
          # IHR - sets result variable so that it is not writing over a previous output & supplies additional text for the output
          
          result.grid(row = 13, column = 5)
          #TJA - Se will output the desired input and plots to row position 8.
      
      elif column == 'MIM Number':
        #TJA - will run this if statement if user selected MIM Number
        
        if info[5] == '-':
        
        
          result = tk.Label(self.master, text = 'The MIM number of this gene is 0.')
          # IHR - sets result variable so that it is not writing over a previous output & supplies text for the output
          
          result.grid(row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
        
        else:
          
          result = tk.Label(self.master, text = 'The MIM number for this gene is ' + info[5])
          # IHR - sets result variable so that it is not writing over a previous output & supplies additional text for the output
          
          result.grid(row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
      
      elif column == 'Uncertain Number': #Not sure if that mutation caused the variation in gene
        #TJA - will run this if statement if user selected Uncertain Number
        
        if info[6] == '-':
        
          result = tk.Label(self.master, text = 'The number of reports that were uncertain that mutation caused a variation in this gene is 0.')
          # IHR - sets result variable so that it is not writing over a previous output & supplies text for the output

          result.grid (row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
        
        
        else:
        
          result = tk.Label(self.master, text = 'The number of reports that were uncertain that mutation caused a variation in this gene are ' + info[6])
          # IHR - sets result variable so that it is not writing over a previous output & supplies additional text for the output

          result.grid (row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.

      
      elif column == 'Number With Conflicts': #differences between number of people who submitted that a something in the gene could bengin but also said it could be pathogenic 
        #TJA - will run this if statement if user selected Number With Conflicts
        if info[7] == '-':
        
          result = tk.Label(self.master, text = 'The number of conflicts in reports of pathogenic versus benign is 0.')
          # IHR - sets result variable so that it is not writing over a previous output & supplies text for the output

          result.grid (row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
        
        else:
        
          result = tk.Label(self.master, text = 'The number of conflicts in reports of pathogenic versus benign are ' + info[7])
          # IHR - sets result variable so that it is not writing over a previous output & supplies additional text for the output

          result.grid (row = 13, column = 5)
          #TJA - Sets a GUI label result that will output the desired input and plots to row position 8.
    
    def get_stats(self, *args):
      '''
      Author: TJA

      Funtion that summarizes information from the human genome in general if the user doesn't want to specify a gene.

      Arguments:
      self
      *args = the option that the user selected from the drop down menu for exploring ClinVar data

      Returns:
      Depending on the user-inputted selection for *args, will print out a descriptive statement of the desired information as well as the information to the GUI

      '''

      option = self.value_in_gen.get()
      #TJA - sets variable option to the drop-down menu selection
      
      if option == 'Total Variants':
        #TJA - will run this if statement if user selected Total Variants
        output = tk.Label(self.master, text = 'The Total Number of Variants is ' + self.total_var)

        output.grid (row = 6, column = 5)
        #TJA - sets output to the label containing the descriptive statement as well as the corresponding informative method and grids it to row position 6, column position 5
      
      elif option == 'Total Pathogenic Variants':
        #TJA - will run this if statement if user selected Total Pathogenic variants
        
        output = tk.Label(self.master, text = 'The Total Number of Pathogenic Variants is ' + self.total_path_var)
        
        output.grid (row = 6, column = 5)
        #TJA - sets output to the label containing the descriptive statement as well as the corresponding informative method and grids it to row position 6, column position 5
      
      elif option == 'Variants with Uncertain Significance':
        #TJA - will run this if statement if user selected this option from the drop down menu
        output = tk.Label(self.master, text = 'The Total Number of Variants with Uncertain Significance is ' + str(self.total_unsig))
        
        output.grid (row = 6, column = 5)
        #TJA - sets output to the label containing the descriptive statement as well as the corresponding informative method and grids it to row position 6, column position 5
      
      elif option == 'Average Variants per Gene':
        #TJA - will run this if statement if user selected option Average Variants per Gene from drop down menu
        
        output = tk.Label(self.master, text = 'The Average Variants per Gene is ' + self.avg_var)
        output.grid (row = 6, column = 5)
        #TJA - sets output to the label containing the descriptive statement as well as the corresponding informative method and grids it to row position 6, column position 5
      
      elif option == 'All Statistics':
        #TJA - will run this if statement if the user wants a summary of all available statistics
        
        output = tk.Label(self.master, text = 'All Statistics\n' + self.stats_table)
        
        output.grid (row = 7, column = 5)
        #TJA - sets output to the label containing the descriptive statement as well as the corresponding informative method and grids it to row position 6, column position 5. In this case, if the user selected All Statistics, it would print out a table summarizing all available options from this function


def file_parser(file_name):
  
  '''
  Author: TJA
  Reads in the BED file under variable name file_name

  This function reads in a tab-delimited file written in the BED file format and returns the contents as a dictionary

  Arguments:
  file_name - name of the file as a string

  Returns:
  gene_dict - dictionary of the file contents using the gene name as the key and the corresponding columns of data as the paired values

  '''
  
  keys = []
  lines = []
  gene_dict = {}
  #TJA - establishes empty containers for file parsing

  with open(file_name) as file:
    #TJA - opens the file name to be parsed

    for line in file:
      
      line = line.strip()
      #TJA - removes any white space or new line characters
      
      info = line.split('\t')
      #TJA - splits each line in the file on each tab character and stores as local variable info which is a list
      
      lines.append(info[1:])
      #TJA - appends the data from each line into the lines list container, creates a nested lists. Excludes index position 0 since 0 is the gene name
      
      keys.append(info[0])
      #appends the gene name at index position 0 to the keys container
    

    keys.pop(0)
    lines.pop(0)

    keys.pop(0)
    lines.pop(0)
    #TJA - removes the first two lines of the file from the two list containers as they contain the file name and column headers
    
    i = 0
    #TJA - establishes an integer counter i with initial value of 0
    
    for line in lines:
      
      gene_dict[keys[i]] = line
      #TJA - takes a key from the keys list at index position i and the corresponding values line from the line list to create key-value pairs for the gene_dict dictionary

      i += 1
      #TJA - each iteration of for loop adds 1 to the i counter to ensure that the key and line positions match up

      
  return gene_dict
  #TJA - returns the completed gene_dict dictionary

def get_values(mydict): 
  '''
  Author: KTM, JQ
  Reads in a dictionary, in this case, it takes in the dictionary made by the file_parser()

  Function takes in a dictionary and returns a list of the values from the dictionary 

  Args: my_dict, name of dictionary

  Returns: values, a 2 dimensional list of values from dictionary 
  '''
  values = []
  #KTM, JQ - make an empty list
  for key in mydict:
    values.append((mydict[key]))
  return values
  # KTM, JQ - makes an empty list, uses the keys (genes) to select the list of statistics for each gene and adds that into a 2d list 


def get_all_variants(myvalues):
  '''
  Author: KTM, JQ
  Reads in a 2 dimensional list, in this case, it takes in the list made by the get_values()

  Function takes in a 2 dimensional list and returns a sum of all variants in the 2d list, that is the second index in each list element that is part of the bigger list

  Args: myvalues, a 2 dimensional list 

  Returns: interger value of the sum total 
  '''
  total_vars = []
  #KTM, JQ - Makes an empty list to which values for the number of variants (genes) are added from column 3 (index 2) only counts numbers and leaves genes with the '-' 
  for i in myvalues:
    if i[2] == '-':
      pass
    else:
      total_vars.append(i[2])
    new_total_vars = [int(x) for x in total_vars]
    total_variants = sum(new_total_vars)
  return str(total_variants)
  #KTM,JQ - returns total number of variants by iterating through the list of variants for each gene and gets sum of all variants 

def pathogenic_vars(myvalues):
  '''
  Author: KTM, JQ
  Reads in a 2 dimensional list, in this case, it takes in the list made by the get_values()

  Function takes in a 2 dimensional list and returns a sum of all pathogenic variants in the 2d list, that is the fourth index in each list element that is part of the bigger list

  Args: myvalues, a 2 dimensional list 

  Returns: interger value of the sum total of all pathogenic gene variants 
  '''
  total_pathogenic = []
  #KTM - make empty list
  
  for i in myvalues:
   
    if i[4] == '-':
      pass 
    
    else:
      total_pathogenic.append(i[4])

    #KTM, JQ - iterate through values from get_values() function and get just the number of pathogenic variants from the 5th column (4th index) as a list of just numbers and no '-'
    
    new_total_pathogenic = [int(x) for x in total_pathogenic]
    total_pathogenic_vars = sum(new_total_pathogenic)
  
  return str(total_pathogenic_vars)

    #KTM, JQ - make all values of pathogenic genes into intergers and get the sum of all pathogenic variants, return the total number of pathogenic variants as a string

def uncertain_sig_vars(myvalues):
  '''
  Author: KTM, JQ
  Reads in a 2 dimensional list, in this case, it takes in the list made by the get_values()

  Function takes in a 2 dimensional list and returns interger value of the proporttion of all gene variants with uncertain significance among all the documented gene variants, the variants with uncertain sigficance are in the sixth index of each list element that is part of the bigger list

  Args: myvalues, a 2-dimensional list 

  Returns: interger value of the proportion of all gene variants with uncertain significance among all the documented gene variants 
  '''
  
  uncertain_sig = []
  #KTM, JQ - make an empty list 

  for i in myvalues:
    if i[6] == '-':
      pass
    else:
      uncertain_sig.append(i[6])
      #KTM , JQ - Get the values of the variants with uncertain significance that is column 7, index 6  
      new_uncertain_sig = [int(x) for x in uncertain_sig]
      total_vars = int(get_all_variants(myvalues))
      prop_uncertain_sig = sum(new_uncertain_sig)/total_vars
      
      #KTM, JQ - make all the values of variants with uncertain significance for each gene, the 6th index in each list an interger and get the sum of all the intergers in that list
      
  return prop_uncertain_sig

def average_vars(myvalues):
  '''
  Author: KTM, JQ
  Reads in a 2 dimensional list, in this case, it takes in the list made by the get_values()

  Function takes in a 2 dimensional list and returns the average number of variants for each gene in the 2d list, the number of variants for each gene is the second index in each list element that is part of the bigger list

  Args: myvalues, a 2 dimensional list 

  Returns: interger value of average variants for each gene 
  '''
  variants = []

  total_vars = int(get_all_variants(myvalues))
  #KTM, JQ - make an empty list, run the get all variants function to get all values of gene variants and make them intergers
  for i in myvalues:
    variants.append(i[2])
    num_variants = len(variants)
  #KTM, JQ - get all the gene variants in a list, get the length of that list to get all genes in the dictionary 
  average_variants_pergene = total_vars/ num_variants
  
  return str(average_variants_pergene)
  #KTM, JQ - divide the total number of variants by total number of genes and get average number of variants per gene as a string

  

def getall_stats(myvalues):
  '''
  Author: KTM 
  Reads in a 2 dimensional list, in this case, it takes in the list made by the get_values()

  Function takes in a 2 dimensional list, runs the functions total_variants(), total_pathogenic_vars(), prop_uncertain_sig(), average_vars_pergene() and gathers returns a list of all numbers outputted by these functions in the order that they are run

  Args: myvalues, a 2 dimensional list 

  Returns: a list of 4 numbers  
  '''

  total_variants = get_all_variants(myvalues)
  total_pathogenic_vars = pathogenic_vars(myvalues)
  prop_uncertain_sig = uncertain_sig_vars(myvalues)
  average_vars_pergene = average_vars(myvalues)
  #OPT, KTM - retrieves all data points for a list by calling the necessary functions

  mystats =  [total_variants, total_pathogenic_vars, prop_uncertain_sig, average_vars_pergene]
  #OPT, KTM - Creates a list of the values retrieved above using the functions
  summary_stats= ["Total\nvariants", "Pathogenic\nalleles", "Uncertain\nsignificance", "Variants\nper-gene"]
  #OPT, KTM - Creates a second list for labelling each specific part of the mystats list
  table = [summary_stats, mystats]
  #OPT, KTM - Creates a nested list of both the labels and the actual values  
  return table



def create_table(table): 
  
  '''
  Author: KTM, JQ
  Reads in a list of numbers, in this case, list contains all summary statistics gathered getall_stats() function

  Function takes  list and returns a table of summary statistics 

  Args: table, is a list to be used to make a table

  Returns: returns a table  
  '''
  
  mytable = tabulate(table, headers='firstrow', tablefmt= "simple")
  #KTM, JQ - creates a table from a 2d list using the tabulate function from the tabulate package
  return mytable


def main():

  root = tk.Tk()

  root.title('ClinVar')

  genes_gui = Genes(root)

  root.mainloop()

if __name__ == '__main__':
  main()