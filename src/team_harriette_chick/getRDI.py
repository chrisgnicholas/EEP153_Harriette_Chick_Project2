import pickle
import pandas as pd


DRIs = None
with open('data/diet.pickle', 'rb') as fp:
    DRIs = pickle.load(fp)

def getRDIColumns():
    """Get the columns of a returned RDI."""
    return ['Energy',
            'Protein',
            'Fiber, total dietary',
            'Folate, DFE',
            'Calcium, Ca',
            'Carbohydrate, by difference',
            'Iron, Fe',
            'Magnesium, Mg',
            'Niacin',
            'Phosphorus, P',
            'Potassium, K',
            'Riboflavin',
            'Thiamin',
            'Vitamin A, RAE',
            'Vitamin B-12',
            'Vitamin B-6',
            'Vitamin C, total ascorbic acid',
            'Vitamin E (alpha-tocopherol)',
            'Vitamin K (phylloquinone)',
            'Zinc, Zn']

def getBin(age: int):
    """Get the correct age string for our table."""
    # just brute force for now
    if (age > 0) and (age <= 3):
        return('1-3')
    if (age > 3) and (age <= 8):
        return('4-8')
    if (age > 8) and (age <= 13):
        return('9-13')
    if (age > 13) and (age <= 18):
        return('14-18')
    if (age > 18) and (age <= 30):
        return('19-30')
    if (age > 30) and (age <= 50):
        return('31-50')
    if (age > 50):
        return('51+')
 
def getRDI(age: int, sex: str):
    """Get the recommended daily requirement for an individual.

    Parameters:
        age: the age of the individual

        sex: one of c(child) m(male) or f(female)

    Returns:
        a Pandas Series of 'Nutrition' for the individual, of:
            Energy
            Protein
            Fiber, total dietary
            Folate, DFE
            Calcium, Ca
            Carbohydrate, by difference
            Iron, Fe
            Magnesium, Mg
            Niacin
            Phosphorus, P
            Potassium, K
            Riboflavin
            Thiamin
            Vitamin A, RAE
            Vitamin B-12
            Vitamin B-6
            Vitamin C, total ascorbic acid
            Vitamin E (alpha-tocopherol)
            Vitamin K (phylloquinone)
            Zinc, Zn
        """
    if (age < 1) or (age > 120):
        raise ValueException("age must be valid int between 1 and 120")

    if sex.upper() not in ['C', 'M', 'F']:
        raise ValueException(f'invalid sex {sex}')

    bin = getBin(age)
    if bin == '1-3':
        sex = 'C'

    binStr = sex.upper() + ' ' + bin
    ret = DRIs['diet_minimums'][binStr]
    retSeries = pd.Series(ret)
    return retSeries
