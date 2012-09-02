# -*- coding: iso-8859-1 -*-
#
#       untitled.py
#       Copyright 2010 Marc Vollmer (modified by Rene Liebscher)
#       Copyright 2012 Danny E Vasconez <dannyvasconeze@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       
import fuzzy.System
import math
"""\package gamepad
   \brief libreria para utilizar el controlador difuso
   \details Controlador difuso realizado con PyFuzzy
   \authors   Danny Vasconez
   \version   0.0.1
   \date      2012
   \pre       pyfuzzy
   \bug       Ninguno
   \warning   Ninguno
   
"""
"""
   \section intro Ejemplo de uso
   En el ejemplo se muestra como utilizar esta libreria
   \verbinclude ejemplo_difuso
"""
def _createSystem():
    """
    \brief Crea el conjunto de reglas y valores para el controlador
    \details Este comando no es necesario utilizarlo
    """
    from fuzzy.InputVariable import InputVariable
    from fuzzy.OutputVariable import OutputVariable
    from fuzzy.fuzzify.Plain import Plain
    from fuzzy.defuzzify.COG import COG
    from fuzzy.Adjective import Adjective
    from fuzzy.set.Polygon import Polygon

    system = fuzzy.System.System()

    #----------------------------------------------------------------------------------------------------------------
    # Valores de entrada
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
    # Valores de salida
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
    # Reglas
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
    \class FuzzyController.FuzzyController2
    \brief Es la clase encargada de realizar los calculos para el controlador
    \details  Se utilizo el esqueleto encontrado en la pagina de pyfuzzy
    """

    def __init__(self):
        """
        \brief Carga valores a las variables necesarias para funcionar la libreria
        \details  este comando no es necesario utilizarlo es usado al instanciar la clase
        \param self este parametro no es necesario escribir
        """
        self.system = _createSystem()


    def calculate(self,input={},output={'vel':0.0}):
        """
        \brief El controlador difuso con sus entradas y salidas
        \details  Sirve realizar el calculo de la salida dependiendo de la entrada
        \param self este parametro no es necesario escribir
        \param input variable de entrada debe ser un diccionario input={"error":500} por ejemplo
        \param output variable de salida debe ser un diccionario output={"vel":500} por ejemplo no es necesario crearlo a menos que se desee tener un valor de arranque diferente de cero
        \return output
        """
        if input["error"]> 5000:
            input["error"] = 5000
        elif input["error"]< -5000:
            input["error"] = -5000
        self.system.calculate(input,output)

        return output

    def createDoc(self,directory):
        """
        \brief Crea documentacion de todas las variables.
        \details Crea documentacion de todas las variables.
        \param self este parametro no es necesario escribir
        \param directory direccion en donde se van a generar los archivos
        """
        from fuzzy.doc.plot.gnuplot import doc
        d = doc.Doc(directory)
        d.createDoc(self.system)
        d.overscan=0
        d.create3DPlot(self.system,"error","vel",{"X":0.,"dX_dT":0.})

    def createDot(self,directory):
        """
        \brief Crea documentacion de las reglas.
        \details Crea documentacion de las reglas.
        \param self este parametro no es necesario escribir
        \param directory direccion en donde se van a generar los archivos
        """
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
	"""
	\brief Controlador con setpoint, valor de entrada
	\details Crea documentacion de las reglas.
	\param setpoint
	\param valor
	\param error
	\param prueba 
	"""
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
