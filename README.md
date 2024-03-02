# EEP153_Harriette_Chick_Project2

## Topic & Goals
Our project focused on determining the most affordable diet in a public school. We are basing our pricing on the 'The USDA Foods in Schools program', as per: https://www.fns.usda.gov/usda-fis/school, supports domestic nutrition programs and American agricultural producers through purchases of 100% American-grown and -produced foods for use by schools and institutions participating in the following nutrition programs:

[National School Lunch Program (NSLP)] (https://www.fns.usda.gov/nslp/national-school-lunch-program-nslp)
[Child and Adult Care Food Program (CACFP)] (https://www.fns.usda.gov/cacfp)
[Summer Food Service Program (SFSP)] (https://www.fns.usda.gov/sfsp/summer-food-service-program)

Within this study, our focal point centered on assessing the cost-effectiveness of dietary solutions specifically tailored for 12-year-old middle school students. Our objective was to identify and recommend practical strategies that not only meet nutritional requirements but also address financial constraints commonly encountered in public school environments.

## File Structure
team_notebook: This is the main notebook which contains all of our overarching relevant code. 

    load_data: This file contains the code which loads our price data from the USDA and the DRI data from the US governments's recommendations. This file is referenced in the code of team_notebook.

    getPrices: This file contains the code which solves the subsistence cost problem. This file is referenced in the code of get_diet.

    get_diet: This file contains the code that prints the solution to the subsistence problem which was calculated in the file "getPrices". This file is referenced in the code of team_notebook. 

    examine_price_changes: This file contains the code that outputs the plot examining the effect of changes in log costs of different ingredients on the cost of the minimum cost diet. This file is referenced in the code of team_notebook. 

    examine_composition: This file contains the code that outputs the plot examining the effect of changes in the cost of 'liquid eggs' on the composition of the minimum cost diet. This file is referenced in the code of team_notebook. 

    constrained_diet_composition: This file contains the code that recalculates the earlier plot with a constraint that total weight of diet must be less that 12 hectograms (1.2 kg). This file is referenced in the code of team_notebook. 


## Project Logistics
### Meet Team Harriette Chick

Dojun Kim (email: kim.dojun@berkeley.edu; github: @kimnmd)

Kevin Kim (email: kevinkim1942@berkeley.edu; github:kevinkim1942)

Angela Chen (email: akchen@berkeley.edu; github: angiechen17)

Yazda Cokgor (email:yscokgor@berkeley.edu; github:yscokgor)

Malena Buffagni (email:malenabuffagni@berkeley.edu; github:malenabuffagni)

Chris Nicholas (email:chrisgnicholas@berkeley.edu; github:chrisgnicholas)


## External Links
Team Harriette Chick Food Price Data Sheet:https://docs.google.com/spreadsheets/d/1UrvYh0ynYkAa8Ye0ncmNddnVDfc4Do2F/edit?usp=sharing&ouid=117538634223013877380&rtpof=true&sd=true

#### Side Note
This is based in large part on the lecture2 notebook, but broken into more modular units. The core "solve_subsistence_problem" routine has been broken out in a Python module, in the src subdirectory.

Other chunks of functionality to read data and generate plots have been broken out as companion notebooks.

Note that we are using flake8 (https://flake8.pycqa.org/en/2.5.5/) to check for proper formatting of our module code as per PEP8 (https://peps.python.org/pep-0008/)

### Due Dates
Code Rough Draft: March 1

Code Review: March 5

Potluck: March 5

Presentations: March 8



