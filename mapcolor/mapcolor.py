'''
mapcolor.py
Code for a map-coloring problem solver 
'''
import sys
import re
import itertools as it
from collections import defaultdict

class MapColor:
    def __init__(self, neighborpairs, colors):
        '''
        
        '''
        assert isinstance(neighborpairs, str), 'neighborpairs must be a string'
        assert isinstance(colors, list), 'colors must be a list of strings'
        self.color_list = colors

        self.neighbors = defaultdict(list)
        self.neighbor_list = []
        specs = [spec.split(':') for spec in neighborpairs.split(';')]

        vset = set()
        for (A, Aneigh) in specs:
            A = A.strip()
            for B in Aneigh.split():
                self.neighbors[A].append(B)
                self.neighbors[B].append(A)
                self.neighbor_list.append((A,B))
                vset.add(A)
                vset.add(B)

        self.variable_list = list(vset)
        self.bf_count = 0
        self.bt_count = 0

    def solve_brute_force(self):
        '''Brute force solver for map coloring. Simply uses a DFS to try all combinations of colors with
        the map locations we have until it finds one that is a legal coloring.
        '''
        assignment = {}
        self.rec_brute_force(assignment)
        return assignment

    def rec_brute_force(self, assignment):
        '''Recursive helper for brute force
            assignment is a dictionary from variables to values
        '''
        var = self.select_unassigned_variable(assignment)
        if var == None:
            return self.is_solution(assignment)
        for val in self.color_list:
            assignment[var] = val
            self.bf_count += 1
            result = self.rec_brute_force(assignment)
            if result != False:
                return True
            del assignment[var]
        return False

    def is_solution(self, assignment):
        '''Checks whether a given assignment is actually a solution.
        '''
        for pair in self.neighbor_list:
            if assignment[pair[0]] == assignment[pair[1]]:
                return False
        return True

    def select_unassigned_variable(self, assignment, domains = None):
        '''Selects a variable that has not yet been given a value according to
        the given assignment.
        Currently this just selects the first variable in variable_list that
        has not yet been given a value in the assignment. 
        Large increases in efficiency are possible with some more intelligent 
        selection criteria, but it isn't necessary to do this for the map-coloring problem.
        '''
        if domains == None:
            for var in self.variable_list:
                if var not in assignment:
                    return var
        return None

    def solve_backtrack_search(self):
        '''A helper function that sets up our domains and initial assignment, then 
        calls a recursive backtracking search that will do the hard work.
        
        You should not need to change this function.
        '''
        domains = {}
        for var in self.variable_list:  #var = State in States
            domains[var] = self.color_list[:]   #assigns list of domains to variable; domains[var] = {R,G,B}; 
        result = self.backtrack({}, domains)
        if self.is_solution(result):
            return result
        else:
            return "Error! Backtrack returned an assignment that is not a solution"

    def backtrack(self, assignment, domains):
        if len(assignment) == len(domains):#check if assignment is same length as domains
            return assignment
        var = self.select_unassigned_variable(assignment)   #var is a state
        for val in domains[var]:
            assignment[var] = val   #adds color to our assignment dict, assignment[var]
            saved = domains[var]
            domains[var] = [val]
            inferences = self.ac3(domains)  #inferences = {} of all things removed
            if inferences != False:
                self.bt_count += 1
                result = self.backtrack(assignment, domains)
                if result != False:
                    return result
            del assignment[var] #remove {var = value} and inferences from assignment
            #add inferences back into domains
            if inferences != False:
                for key, values in inferences.items():
                    domains[key].extend(values)
            domains[var] = saved 
        return False
        
        
    def ac3(self, domains):
        q = self.neighbor_list  #list of state pairs as tuples
        for pair in q:
            q = q + [(pair[1], pair[0])]
        removeddict = {x:[] for x in domains}   #populate our dict with
        while len(q) > 0:
            (xi, xj) = q.pop() #assigns first tuple value in list to tuple (xi,xj)
            removedlist = self.revise(xi, xj, domains)
            if len(removedlist) > 0:
                if len(domains[xi]) == 0:
                    if removeddict != False:
                        for key, values in removeddict.items():
                            domains[key].extend(values)
                        domains[xi].extend(removedlist)
                    return False
                for xk in self.neighbors[xi]:      
                    if xk != xj:
                        q.append((xk, xi))
            removeddict[xi].extend(removedlist)
        return removeddict
    
    
    def revise(self, xi, xj, domains):
        removedlist = []
        for valx in domains[xi]:    #valx is a color
            cansatisfy = False
            for valy in domains[xj]:
                if valx != valy:
                    cansatisfy = True
            if cansatisfy == False:
                removedlist.append(valx)
        for val in removedlist:
            domains[xi].remove(val)
        return removedlist
                

def main():
    # m0: Washington, Oregon, Idaho, Nevada. Can we color them with 3 colors?
    m0 = MapColor("""WA: OR ID; OR: ID NV; ID: NV""" , ['R', 'G', 'B'])
    #print(m0.solve_brute_force())
    print("Brute force assignments made: " + str(m0.bf_count))
    print("---------------------------------------------")
    print(m0.solve_backtrack_search())
    print("Backtrack assignments made: " + str(m0.bt_count))


    # m1: Washington, Oregon, Idaho, Montana, Nevada, California, Utah, Colorado, Wyoming, New Mexico and Arizona
    m1 = MapColor('''WA: OR ID;
                     OR: ID NV CA;
                     CA: NV AZ;
                     NV: UT AZ;
                     ID: NV MT UT WY;
                     UT: AZ CO WY;
                     CO: WY NM;
                     WY: MT;
                     NM: AZ''', 
                     ['R', 'G', 'B', 'Y'])
    #print(m1.solve_brute_force())
    print("Brute force assignments made: " + str(m1.bf_count))
    print(m1.solve_backtrack_search())
    print("Backtrack assignments made: " + str(m1.bt_count))

    # m2: m1 plus North and South Dakota
    m2 = MapColor('''WA: OR ID;
                     OR: ID NV CA;
                     CA: NV AZ;
                     NV: UT AZ;
                     ID: NV MT UT;
                     UT: AZ CO WY;
                     CO: WY NM;
                     WY: MT SD;
                     NM: AZ;
                     MT: ND SD;
                     ND: SD''', 
                     ['R', 'G', 'B', 'Y'])
    #print(m2.solve_brute_force())
    print("Brute force assignments made: " + str(m2.bf_count))
    print(m2.solve_backtrack_search())
    print("Backtrack assignments made: " + str(m2.bt_count))

    # mgh is the Goldner-Harary Graph
    mgh = MapColor('''A: B C D E F G H K;
                      B: E F;
                      C: F G;
                      D: E K;
                      E: F I;
                      F: G I J;
                      G: H J K;
                      H: K;
                      I: K;
                      J: K ''', ['R', 'G', 'B', 'Y'])
    #print(mgh.solve_brute_force())
    print("Brute force assignments made: " + str(mgh.bf_count))

    # entire usa. don't even think about brute forcing this
    usa = MapColor('''WA: OR ID; OR: ID NV CA; CA: NV AZ; NV: ID UT AZ; ID: MT WY UT;
        UT: WY CO AZ; MT: ND SD WY; WY: SD NE CO; CO: NE KA OK NM; NM: OK TX;
        ND: MN SD; SD: MN IA NE; NE: IA MO KA; KA: MO OK; OK: MO AR TX;
        TX: AR LA; MN: WI IA; IA: WI IL MO; MO: IL KY TN AR; AR: MS TN LA;
        LA: MS; WI: MI IL; IL: IN KY; IN: OH KY; MS: TN AL; AL: TN GA FL;
        MI: OH IN; OH: PA WV KY; KY: WV VA TN; TN: VA NC GA; GA: NC SC FL;
        PA: NY NJ DE MD WV; WV: MD VA; VA: MD DC NC; NC: SC; NY: VT MA CT NJ;
        NJ: DE; DE: MD; MD: DC; VT: NH MA; MA: NH RI CT; CT: RI; ME: NH;
        HI: ; AK: ''', list('RGBY'))
    print(usa.solve_backtrack_search())
    print("Backtrack assignments made: " + str(usa.bt_count))

    # USA can't actually be colored with 3 colors. But if you remove troublesome states
    # California and Ohio, you can in fact color it with 3 colors.
    usa3 = MapColor('''WA: OR ID; OR: ID NV; NV: ID UT AZ; ID: MT WY UT;
        UT: WY CO AZ; MT: ND SD WY; WY: SD NE CO; CO: NE KA OK NM; NM: OK TX;
        ND: MN SD; SD: MN IA NE; NE: IA MO KA; KA: MO OK; OK: MO AR TX;
        TX: AR LA; MN: WI IA; IA: WI IL MO; MO: IL KY TN AR; AR: MS TN LA;
        LA: MS; WI: MI IL; IL: IN KY; IN: KY; MS: TN AL; AL: TN GA FL;
        MI: IN; KY: WV VA TN; TN: VA NC GA; GA: NC SC FL;
        PA: NY NJ DE MD WV; WV: MD VA; VA: MD DC NC; NC: SC; NY: VT MA CT NJ;
        NJ: DE; DE: MD; MD: DC; VT: NH MA; MA: NH RI CT; CT: RI; ME: NH;
        HI: ; AK: ''', list('RGB'))
    print(usa3.solve_backtrack_search())
    print("Backtrack assignments made: " + str(usa3.bt_count))

    # Color France's regions
    france = MapColor(''''AL: LO FC; AQ: MP LI PC; AU: LI CE BO RA LR MP; BO: CE IF CA FC RA
        AU; BR: NB PL; CA: IF PI LO FC BO; CE: PL NB NH IF BO AU LI PC; FC: BO
        CA LO AL RA; IF: NH PI CA BO CE; LI: PC CE AU MP AQ; LO: CA AL FC; LR:
        MP AU RA PA; MP: AQ LI AU LR; NB: NH CE PL BR; NH: PI IF CE NB; NO:
        PI; PA: LR RA; PC: PL CE LI AQ; PI: NH NO CA IF; PL: BR NB CE PC; RA:
        AU BO FC PA LR''', list('RGBY'))
    print(france.solve_backtrack_search())
    print("Backtrack assignments made: " + str(france.bt_count))

    
if __name__ == '__main__':
    main()
