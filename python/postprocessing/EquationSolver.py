import math as math
import ROOT
import ROOT.TMath as TMath
import cmath
import string
import io

def EqSolv(a1, a2, a3, a4):
    if type(a1) != float and type(a1) != int:
        if type(a1) == list:
            a = a1[0]
            b = a1[1]
            c = a1[2]
            d = a1[3]
            result = []
        elif type(a1) == dict:
            a = a1['a']
            b = a1['b']
            c = a1['c']
            d = a1['d']
            result = {}
    else:
        a = a1
        b = a2
        c = a3
        d = a4
        result = []

   
    if a != 0.:
        q = (3.*a*c - b*b)/(9.*a*a)
        r = (9.*a*b*c - 27.*a*a*d - 2.*b**3.)/(54.*a**3.)
        Delta = q**3. + r**2.
    
        if Delta <= 0: #da testare
            rho = (-(q**(3)))**(0.5)
            theta = math.acos(r/rho)
            s = cmath.rect((-q)**(0.5), theta/3.0)
            t = cmath.rect((-q)**(0.5), -theta/3.0)
            
    
        if Delta > 0:
            args = r+(Delta)**(0.5)
            argt = r-(Delta)**(0.5)
            signs = math.copysign(1, args)
            signt = math.copysign(1, argt)
            s = complex(signs*TMath.Power(abs(args), 1./3), 0)
            t = complex(signt*TMath.Power(abs(argt), 1./3), 0)
        
        rpar = b/(3.*a)
        x1 = s + t + complex(-rpar, 0)
        x2 = (s+t)*complex(-0.5, 0) - complex(rpar, 0) + (s-t)*(1j)*complex((3.**(0.5))/2., 0)
        x3 = (s+t)*complex(-0.5, 0) - complex(rpar, 0) - (s-t)*(1j)*complex((3.**(0.5))/2., 0)

    

        if abs(x1.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x1': x1.real})
            else:
                result.append(x1.real)
        if abs(x2.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x2': x2.real})
            else:
                result.append(x2.real)
        if abs(x3.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x3': x3.real})
            else:
                result.append(x3.real)            

        return result
    
    else:
        print 'p1'
        result = None
        return result
'''    
    #return result
top = EqSolv(8.5, 9.0, 11.467, -10984)
print top
'''