/*********************************************
 * OPL 22.1.0.0 Model
 * Author: m_vol
 * Creation Date: 26 Nov 2022 at 10:30:43
 *********************************************/

float Capacity = ...;

int NbItems = ...;
range Items = 1..NbItems;

int NbGroups = ...;
range Groups = 1..NbGroups;

float Value[Items] = ...;
float Weight[Items]= ...;
int Group[Items] = ...;

dvar int+ Take[Items] in 0..1;

maximize
  sum(i in Items) Take[i] * Value[i];
  
subject to {
    c1:
      sum(i in Items) Take[i] * Weight[i] <= Capacity;
    c2:
      forall(g in Groups) sum(i in Items: Group[i] == g) Take[i] == 1;     
}


tuple TakeSolutionT{ 
	int Groups;
	int Items;
	float Weight;
};

{TakeSolutionT} TakeSolution = {<Group[i0],i0,Weight[i0]> | i0 in Items: Take[i0] == 1};
execute{ 
	writeln(TakeSolution);
}