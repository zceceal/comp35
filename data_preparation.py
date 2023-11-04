import pandas as pd
import matplotlib.pyplot as plt

# The csv data file of Dog populations in the city of Zurich since 2015 to 2023
csv_file_path = 'dataset.csv'

# List of columns selected with 0-based index
columns_to_select = [0, 3, 8, 13, 15, 18, 23, 24, 27]

# Read the data csv file containing all of the information 
data = pd.read_csv(csv_file_path)

# Remove rows with age of dog owner as 999 which refers to uknown
data = data[data['AlterV10Cd'] != 999]

# Selecting the specific columns
selected_data = data.iloc[:, columns_to_select]

# Defining the headers for the new columns in English for easier manipulation
new_headers = ['Year', 'Age of dog owner', 'Gender of dog owner', 'City district dog owner', 'Primary breed of dog', 'Mixed breed', 'Year of birth of the dog', 'Age of the dog', 'Code gender of the dog']

# Renaming the columns of the selected data
selected_data.columns = new_headers

# Defining the path and name for the new CSV file with data prepared for manipulation
new_csv_file_path = 'dataset_prepared.csv'

# Writing the selected data to a new CSV file with headers
selected_data.to_csv(new_csv_file_path, index=False)

# Printing a message confirming the specific columns have been selected, inserted into a new csv file and the new headers have been defined 
print(f'Selected data with headers has been written to {new_csv_file_path}.')

# Loading the data prepared for the analysis
data = pd.read_csv('dataset_prepared.csv')

# Filtering the data for year 2023
data_2023 = data[data['Year'] == 2023]

## Making a pie chart visually describing the percentage of different dog breeds found in Zurich in 2023
# Counting the occurrences of the different primary breeds of dog
breed_counts = data_2023['Primary breed of dog'].value_counts()

# Calculating the percentage of each primary dog breed
breed_percentages = (breed_counts / breed_counts.sum()) * 100

# Filtering the dog breeds which have a percentage greater than 1% and conjointly calculating the percentage of the other dog breeds ('Other')
top_breeds = breed_percentages[breed_percentages > 1]
percentage_other = breed_percentages[breed_percentages <= 1].sum()

# Creating a new frame of data for the top breeds (dog breeds which have a percentage greater than 1%) and the 'Other' category
combined_breeds = pd.concat([top_breeds, pd.Series([percentage_other], index=['Other (breeds with a percentage lower than 1%)'])])

# Generating a Pie Chart describing the percentage of different dog breeds found in Zurich in 2023
plt.figure(figsize=(12, 6))
plt.pie(combined_breeds, labels=combined_breeds.index)
plt.title('Percentage of Dog Breeds in 2023')
plt.show()

## Making a plot (line graph) of the percentage of men and women dog owners in Zurich and displaying how it has changed over time (2015 to 2023)
# Grouping the data by year and gender of the dog owner and counting the occurrences
gender_counts = data.groupby(['Year', 'Gender of dog owner']).size().unstack(fill_value=0)

# Adding together the total count of female and male dog owners for each year (2015 to 2023)
total_counts = gender_counts.sum(axis=1)

# Calculating the percentage of men and women dog owners in each year (2015 to 2023)
percentage_men = (gender_counts[1] / total_counts) * 100
percentage_women = (gender_counts[2] / total_counts) * 100

# Generating a plot of the percentage of female and male dog owners over the years (2015 to 2023)
plt.figure(figsize=(10, 6))
plt.plot(percentage_men.index, percentage_men.values, marker='o', label='Men', color='blue')
plt.plot(percentage_women.index, percentage_women.values, marker='o', label='Women', color= 'red')
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Percentage of Men and Women Dog Owners in Zurich (2015-2023)')
plt.grid(True)
plt.show()

## Making a bar chart of the number of dog owners in Zurich in 2023 based on the age group
# Grouping the data by the age group of the dog owner and counting the occurrences
age_group_counts = data_2023['Age of dog owner'].value_counts().sort_index()

# Generating a plot (bar chart) of the number of dog owners based on the age group they are in, in 2023
plt.figure(figsize=(10, 6))
age_group_counts.plot(kind='bar', color='red')
plt.xlabel('Age Group')
plt.ylabel('Frequency')
plt.title('Frequency of Dog Owners by Age Group in 2023')
plt.grid(True)
plt.show()

## Making a plot (line graph) describing how the number of pedigree dogs has changed over time in Zurich (2015 to 2023)
# Filtering the data for 2015 to 2023 for pedigree dogs ('Rassehund' in German and translates to 'Pedigree')
pedigree_dogs = data[data['Mixed breed'] == 'Rassehund']

# Grouping the data for pedigree dogs by year and counting the number of pedigree dogs
pedigree_dog_counts = pedigree_dogs.groupby('Year').size()

# Generating a plot (line graph) which displays the change in number of pedigree dogs over time in Zurich (2015 to 2023)
plt.figure(figsize=(12, 6))
plt.plot(pedigree_dog_counts.index, pedigree_dog_counts.values, marker='o', color='red')
plt.xlabel('Year')
plt.ylabel('Number of Pedigree Dogs')
plt.title('Change in Number of Pedigree Dogs Over Time')
plt.grid(True)
plt.show()

## Making a bar chart for the female pedigree dog preference by city district for 2023
# Filtering the data for female gender and the pedigree dogs ('Rassehund' in German and translates to 'Pedigree')
data_2023_female_dogs = data_2023[(data_2023['Code gender of the dog'] == 2) & (data_2023['Mixed breed'] == 'Rassehund')]

# Grouping the data by city district of the dog owner and the primary breed of the dog 
# Counts the number of occurrences for each unique combination of district and breed 
# Data for 'Primary breed of dog' is converted into columns to facilitate interpretation and sets a value of 0 if there are any missing values
district_breed_counts = data_2023_female_dogs.groupby(['City district dog owner', 'Primary breed of dog']).size().unstack(fill_value=0)

# Filtering the data in order to only include in the bar chart the 5 most common dog breeds for each city district and applying it to every row of data
district_breed_counts = district_breed_counts.apply(lambda x: x.nlargest(5), axis=1)

# Defining colours in order to avoid repetition and facilitate visual representation and understanding
colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'DeepPink', 'gray', 'olive', 'lightblue', 'darkblue', 'darkorange', 'lightgreen', 'darkred', 'hotpink', 'MediumVioletRed', 'lightpink', 'lightgray', 'IndianRed', 'Crimson', 'FireBrick', 'turquoise']

# Generating a bar chart that displays the female pedigree dog breed preference by city district in 2023
district_breed_counts.plot(kind='bar', stacked=True, figsize=(12, 6), color=colors)
plt.xlabel('City District')
plt.ylabel('Count')
plt.ylim(0, 100)
plt.title('Top 5 Pedigree Female Dog Breeds by City District in 2023')
plt.legend(title='Breed of Dog', fontsize='xx-small', loc='upper center', ncol =6)
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

## Making a bar chart for the male pedigree dog preference by city district for 2023
# Filtering the data for male gender and the pedigree dogs ('Rassehund' in German and translates to 'Pedigree')
data_2023_male_dogs = data_2023[(data_2023['Code gender of the dog'] == 1) & (data_2023['Mixed breed'] == 'Rassehund')]

# Grouping the data by city district of the dog owner and the primary breed of the dog 
# Counts the number of occurrences for each unique combination of district and breed 
# Data for 'Primary breed of dog' is converted into columns to facilitate interpretation and sets a value of 0 if there are any missing values
district_breed_counts = data_2023_male_dogs.groupby(['City district dog owner', 'Primary breed of dog']).size().unstack(fill_value=0)

# Filtering the data in order to only include in the bar chart the 5 most common dog breeds for each city district and applying it to every row of data
district_breed_counts = district_breed_counts.apply(lambda x: x.nlargest(5), axis=1)

# Generating a bar chart that displays the male pedigree dog breed preference by city district in 2023
district_breed_counts.plot(kind='bar', stacked=True, figsize=(12, 6), color=colors)
plt.xlabel('City District')
plt.ylabel('Count')
plt.ylim(0, 100)
plt.title('Top 5 Pedigree Male Dog Breeds by City District in 2023')
plt.legend(title='Primary Breed of Dog', fontsize='xx-small', loc='upper center', ncol =6)
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

## Making a bar chart for the pedigree dogs by city district in 2023
# Filtering the pedigree dogs ('Rassehund' in German and translates to 'Pedigree')
data_2023_pedigree_dogs = data_2023[data_2023['Mixed breed'] == 'Rassehund']

# Grouping the data of pedigree dogs by city district
# Counts the number of occurrences for each unique combination of city district and pedigree dogs
# Data for 'Mixed breed' is converted into columns to facilitate interpretation and sets a value of 0 if there are any missing values
district_breed_counts = data_2023_pedigree_dogs.groupby(['City district dog owner', 'Mixed breed']).size().unstack(fill_value=0)

# Generate a bar chart to show how the number of pedigree dogs is related to each city district in 2023
district_breed_counts.plot(kind='bar', stacked=True, figsize=(12, 6), color='red')
plt.xlabel('City District')
plt.ylabel('Count')
plt.title('Frequency of pedigree dogs by City District in 2023')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

## Making a bar chart for the age of the pedigree dogs in 2023
# Grouping the data of pedigree dogs by age of the dog
# Counts the number of occurrences for each unique combination of age of the dog and pedigree dogs
# Data for 'Mixed breed' is converted into columns to facilitate interpretation and sets a value of 0 if there are any missing values
pedigree_age_counts = data_2023_pedigree_dogs.groupby(['Age of the dog', 'Mixed breed']).size().unstack(fill_value=0)

# Generating a bar chart to show the number of pedigree dogs in each city district in 2023
pedigree_age_counts.plot(kind='bar', stacked=True, figsize=(12, 6), color='red')
plt.xlabel('Age of the dog')
plt.ylabel('Count')
plt.title('Age of the Pedigree dogs in 2023')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

## Making a bar chart for the age of the pedigree dogs for the chosen breed in 2023, having chosen the gender. In order to get isolated data for a specific gender of interest
# Grouping the data of pedigree dogs by age of the dog
# Counts the number of occurrences for each unique combination of age of the dog and pedigree dogs
# Data for 'Mixed breed' is converted into columns to facilitate interpretation and sets a value of 0 if there are any missing values
chosen_breed = 'Labrador'
female_or_male = 1
data_2023_breed = data_2023[(data_2023['Primary breed of dog'] == chosen_breed) & (data_2023['Mixed breed'] == 'Rassehund') & (data_2023['Code gender of the dog'] == female_or_male)]
pedigree_age_counts = data_2023_breed.groupby(['Age of the dog', 'Mixed breed']).size().unstack(fill_value=0)

if female_or_male == 1:
    gender = "Male"
else:
    gender = "Female"

# Generating a bar chart to show the number of pedigree dogs in each city district in 2023
pedigree_age_counts.plot(kind='bar', stacked=True, figsize=(12, 6), color='red')
plt.xlabel('Age of the dog')
plt.ylabel('Count')
plt.title('Age of 'f'{gender} {chosen_breed} pedigree dogs in 2023')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()
