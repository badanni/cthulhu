# -*- coding: iso-8859-1 -*-

"""Another fuzyy controller for the inverted pendulum.

@author: Marc Vollmer (modified by Rene Liebscher)
"""

#from simulation import Controller

import fuzzy.System
import math

def _createSystem():
    '''
    Definition des Fuzzy-Systems:

        1. Eingangsvariable Phi
        2. Eingangsvariable dPhi_dT
        3. Ausgangsvariable a
        4. Definition der Regeln
    '''
    from fuzzy.InputVariable import InputVariable
    from fuzzy.OutputVariable import OutputVariable
    from fuzzy.fuzzify.Plain import Plain
    from fuzzy.defuzzify.COG import COG
    from fuzzy.Adjective import Adjective
    from fuzzy.set.Polygon import Polygon

    system = fuzzy.System.System()

    #----------------------------------------------------------------------------------------------------------------
    # Definition des Drehwinkels als Eingang
    #----------------------------------------------------------------------------------------------------------------
    input_temp = InputVariable(fuzzify=Plain())

    system.variables["error"] = input_temp

    in1_set = Polygon()
    in1_set.add(x =-6000, y= 0.0) # porque debe iniciar y finalizar en cero
    in1_set.add(x =-5000, y= 1.0)
    in1_set.add(x =-4000, y= 0.5)
    in1_set.add(x =-3000, y= 0.0)
    in1 = Adjective(in1_set)
    input_temp.adjectives["MGN"] = in1

    in2_set = Polygon()
    in2_set.add(x =-4500, y= 0.0)
    in2_set.add(x =-3000, y= 1.0)
    in2_set.add(x =-2000, y= 0.0)
    in2 = Adjective(in2_set)
    input_temp.adjectives["GN"] = in2

    in3_set = Polygon()
    in3_set.add(x =-3000, y= 0.0)
    in3_set.add(x =-2000, y= 1.0)
    in3_set.add(x =-1000, y= 0.0)
    in3 = Adjective(in3_set)
    input_temp.adjectives["N"] = in3

    in4_set = Polygon()
    in4_set.add(x = -2000, y= 0.0)
    in4_set.add(x =-1000, y= 1.0)
    in4_set.add(x =0, y= 0.0)
    in4 = Adjective(in4_set)
    input_temp.adjectives["Z"] = in4

    in5_set = Polygon()
    in5_set.add(x = -1000, y= 0.0)
    in5_set.add(x = 1000, y= 1.0)
    in5_set.add(x = 5000, y= 1.0)
    in5_set.add(x =6000, y= 0.0) # porque debe iniciar y finalizar en cero
    in5 = Adjective(in5_set)
    input_temp.adjectives["P"] = in5

    #----------------------------------------------------------------------------------------------------------------
    # Definition der Horizontalbeschleunigung als Ausgang
    #----------------------------------------------------------------------------------------------------------------
    output_temp = OutputVariable(defuzzify=COG())

    system.variables["vel"] = output_temp
    output_temp.failsafe = 0.0 # let it output 0.0 if no COG available

    out1_set = Polygon()
    out1_set.add(x =-200, y= 0.0) # porque debe iniciar y finalizar en cero
    out1_set.add(x =-120, y= 1.0)
    out1_set.add(x =250, y= 0.0)
    out1 = Adjective(out1_set)  
    output_temp.adjectives["VMB"] = out1

    out2_set = Polygon()
    out2_set.add(x =30, y= 0.0)
    out2_set.add(x =355, y= 1.0)
    out2_set.add(x =600, y= 0.0)
    out2 = Adjective(out2_set)
    output_temp.adjectives["VB"] = out2

    out3_set = Polygon()
    out3_set.add(x = 255, y= 0.0)
    out3_set.add(x = 600, y= 1.0)
    out3_set.add(x = 950, y= 0.0)
    out3 = Adjective(out3_set)
    output_temp.adjectives["VM"] = out3

    out4_set = Polygon()
    out4_set.add(x = 600, y= 0.0)
    out4_set.add(x = 875, y= 1.0)
    out4_set.add(x = 1130,  y= 0.0)
    out4 = Adjective(out4_set)
    output_temp.adjectives["VA"] = out4

    out5_set = Polygon()
    out5_set.add(x = 950, y= 0.0)
    out5_set.add(x = 1300, y= 1.0)
    out5_set.add(x =1500, y= 0.0) # porque debe iniciar y finalizar en cero
    out5 = Adjective(out5_set)
    output_temp.adjectives["VMA"] = out5

    #----------------------------------------------------------------------------------------------------------------
    # Definition der Regeln <<hacer>>
    #----------------------------------------------------------------------------------------------------------------
    from fuzzy.Rule import Rule
    from fuzzy.norm.Min import Min
    from fuzzy.operator.Input import Input
    from fuzzy.operator.Compound import Compound

    rule1 = Rule(adjective=system.variables["vel"].adjectives["VMA"],
                                operator=Input(system.variables["error"].adjectives["MGN"]),
                                )
    system.rules["rule1"]=rule1


    rule2 = Rule(adjective=system.variables["vel"].adjectives["VA"],
                            operator=Input(system.variables["error"].adjectives["GN"],),
                            )
    system.rules["rule2"]=rule2 

    rule3 = Rule(adjective=system.variables["vel"].adjectives["VM"],
                            operator=Input(system.variables["error"].adjectives["N"],),
                            )
    system.rules["rule3"]=rule3 

    rule4 = Rule(adjective=system.variables["vel"].adjectives["VB"],
                            operator=Input(system.variables["error"].adjectives["Z"],),
                            )
    system.rules["rule4"]=rule4 

    rule5 = Rule(adjective=system.variables["vel"].adjectives["VMB"],
                            operator=Input(system.variables["error"].adjectives["P"],),
                            )
    system.rules["rule5"]=rule5 

    return system


#class FuzzyController2(Controller.Controller):
class FuzzyController2():
    """
    Fuzzy controller.
    
    """

    def __init__(self):
        self.system = _createSystem()


    def calculate(self,input={},output={'vel':0.0}):
        '''
        Calculates the output value.
        '''
        if input["error"]> 5000:
            input["error"] = 5000
        elif input["error"]< -5000:
            input["error"] = -5000
        self.system.calculate(input,output)

        return output

    def createDoc(self,directory):
        """Create docs of all variables."""
        from fuzzy.doc.plot.gnuplot import doc
        d = doc.Doc(directory)
        d.createDoc(self.system)
        d.overscan=0
        d.create3DPlot(self.system,"error","vel",{"X":0.,"dX_dT":0.})

    def createDot(self,directory):
        """Create docs of rules."""
        import fuzzy.doc.structure.dot.dot
        import subprocess
        for name,rule in self.system.rules.items():
            cmd = "dot -T png -o '%s/Rule %s.png'" % (directory,name)
            f = subprocess.Popen(cmd, shell=True, bufsize=32768, stdin=subprocess.PIPE).stdin
            fuzzy.doc.structure.dot.dot.print_header(f,"XXX")
            fuzzy.doc.structure.dot.dot.print_dot(rule,f,self.system,"")
            fuzzy.doc.structure.dot.dot.print_footer(f)
        cmd = "dot -T png -o '%s/System.png'" % directory
        f = subprocess.Popen(cmd, shell=True, bufsize=32768, stdin=subprocess.PIPE).stdin
        fuzzy.doc.structure.dot.dot.printDot(self.system,f)

def controlador(setpoint=1000,valor=0,error=None,prueba=0):
	a=FuzzyController2()
	input_aa={"error":-5000}
	salida={}
	if prueba==0:
		input_aa["error"]=setpoint-valor
	else:
		input_aa["error"]=error
	output_aa=a.calculate(input_aa)
	salida=output_aa["vel"]
	return salida

def prueba_de_controlador(graficar=0):
	a=FuzzyController2()
	input_aa={"error":-5000}
	salida={}
	for b in range(10000):
		bb=b-5000
		input_aa["error"]=bb
		output_aa=a.calculate(input_aa)
		salida[b]=output_aa["vel"] #la vel negativa significa que el robot va a retroceder
	if graficar == 1:
		bb=range(10000)
		c=range(10000)
		import Gnuplot
		gp = Gnuplot.Gnuplot(persist=1)
		for b in range(10000):
			bb[b]=b-5000
			c[b]=salida[b]
		data = Gnuplot.Data(bb, c, title='velocidad[mm/s] vs error[mm]')
		gp.plot(data)
		gp.hardcopy(filename="vel_vs_err.png",terminal="png")
		return 0
	else:
		return salida

if __name__ == '__main__':
	## Generar documentacion del controlador
	a=FuzzyController2()
	#a.createDoc("/home/badanni/tesis_programas/fuzzy/programa/doc/")
	a.createDot("/home/badanni/tesis_programas/fuzzy/programa/doc/")
	
	## Prueba para un valor fijo en real es velocidad=
	# controlador(setpoint,valor)
	print controlador(error=-2249.3,prueba=1)
	print controlador(1500,-4000)
	## Pueba para generar todos los valores posibles de respuestas y 
	# almacenarlo en una imagen si el parametro es graficar=1 caso 
	# contrario solo devuelve todos los valores posibles 
	salida=prueba_de_controlador()
