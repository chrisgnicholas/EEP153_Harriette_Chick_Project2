import fooddatacentral as fdc
import warnings
import pandas as pd
import numpy as np
from eep153_tools.sheets import read_sheets
from  scipy.optimize import linprog as lp
import numpy as np
import warnings

def solve_subsistence_problem(FoodNutrients,Prices,dietmin,dietmax,max_weight=None,tol=1e-6):
    """Solve Stigler's Subsistence Cost Problem.

    Inputs:
       - FoodNutrients : A pd.DataFrame with rows corresponding to foods, columns to nutrients.
       - Prices : A pd.Series of prices for different foods
       - diet_min : A pd.Series of DRIs, with index corresponding to columns of FoodNutrients,
                    describing minimum intakes.
       - diet_max : A pd.Series of DRIs, with index corresponding to columns of FoodNutrients,
                    describing maximum intakes.
       - max_weight : Maximum weight (in hectograms) allowed for diet.
       - tol : Solution values smaller than this in absolute value treated as zeros.
       
    """
    try: 
        p = Prices.apply(lambda x:x.magnitude)
    except AttributeError:  # Maybe not passing in prices with units?
        warnings.warn("Prices have no units.  BE CAREFUL!  We're assuming prices are per hectogram or deciliter!")
        p = Prices

    p = p.dropna()

    # Compile list that we have both prices and nutritional info for; drop if either missing
    use = p.index.intersection(FoodNutrients.columns)
    p = p[use]

    # Drop nutritional information for foods we don't know the price of,
    # and replace missing nutrients with zeros.
    Aall = FoodNutrients[p.index].fillna(0)

    # Drop rows of A that we don't have constraints for.
    Amin = Aall.loc[Aall.index.intersection(dietmin.index)]
    Amin = Amin.reindex(dietmin.index,axis=0)
    idx = Amin.index.to_frame()
    idx['type'] = 'min'
    #Amin.index = pd.MultiIndex.from_frame(idx)
    #dietmin.index = Amin.index
    
    Amax = Aall.loc[Aall.index.intersection(dietmax.index)]
    Amax = Amax.reindex(dietmax.index,axis=0)
    idx = Amax.index.to_frame()
    idx['type'] = 'max'
    #Amax.index = pd.MultiIndex.from_frame(idx)
    #dietmax.index = Amax.index

    # Minimum requirements involve multiplying constraint by -1 to make <=.
    A = pd.concat([Amin,
                   -Amax])

    b = pd.concat([dietmin,
                   -dietmax]) # Note sign change for max constraints

    # Make sure order of p, A, b are consistent
    A = A.reindex(p.index,axis=1)
    A = A.reindex(b.index,axis=0)

    if max_weight is not None:
        # Add up weights of foods consumed
        A.loc['Hectograms'] = -1
        b.loc['Hectograms'] = -max_weight
        
    # Now solve problem!  (Note that the linear program solver we'll use assumes
    # "less-than-or-equal" constraints.  We can switch back and forth by
    # multiplying $A$ and $b$ by $-1$.)

    result = lp(p, -A, -b, method='interior-point')

    result.A = A
    result.b = b
    
    if result.success:
        result.diet = pd.Series(result.x,index=p.index)
    else: # No feasible solution?
        warnings.warn(result.message)
        result.diet = pd.Series(result.x,index=p.index)*np.nan  

    return result

bulk_prices_w_lbs = pd.read_csv("../../data/bulk_prices.tsv", sep='\t')

apikey = "rfaOy1m0PNZUGET08nKJvgbOrtpJaP86d8yt6RYh" 

D = {}
count = 0
food_names = bulk_prices_w_lbs.Material_Descr.tolist()
for food_name in food_names:
    try:
        fdc_id = bulk_prices_w_lbs.loc[bulk_prices_w_lbs.Material_Descr==food_name,:].FDC_ID
        int_fdcid = int(fdc_id[count])
        count+=1
        D[food_name] = fdc.nutrients(apikey,int_fdcid).Quantity
        print(f'count: {count} {food_name}')
    except AttributeError: 
        warnings.warn("Couldn't find FDC Code %s for food %s." % (food_name,int_fdcid))        
    except ValueError:
        warnings.warn(f"No code for food {food_name}")
    except Exception as ex:
        warnings.warn(f"something nuts for {food_name}  {ex}")

FoodNutrients = pd.DataFrame(D,dtype=float)

# all items are 1 pound
bulk_prices_w_lbs['FDC Quantity'] = bulk_prices_w_lbs[['Quantity','BaseUoM']].T.apply(lambda x : fdc.units(x['Quantity'],x['BaseUoM']))

bulk_prices_w_lbs['FDC Price'] = bulk_prices_w_lbs['Average_Price']/bulk_prices_w_lbs['FDC Quantity']

bulk_prices_w_lbs.dropna(how='any')

# To use minimum price observed
Prices = bulk_prices_w_lbs.groupby('Material_Descr',sort=False)['FDC Price'].min()

# get DRIs
DRI_url = "https://docs.google.com/spreadsheets/d/1y95IsQ4HKspPW3HHDtH7QMtlDA66IUsCHJLutVL-MMc/"

DRIs = read_sheets(DRI_url)

# Define *minimums*
diet_min = DRIs['diet_minimums'].set_index('Nutrition')

# Define *maximums*
diet_max = DRIs['diet_maximums'].set_index('Nutrition')

group = 'M 19-30'
tol = 1e-6

result = solve_subsistence_problem(FoodNutrients,Prices,diet_min[group],diet_max[group],tol=tol)

print("Cost of diet for %s is $%4.2f per day.\n" % (group,result.fun))

reasonable_amounts = result.diet[result.diet>1e-6]

print(reasonable_amounts)
