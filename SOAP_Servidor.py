# SOAP_Servidor.py
from pysimplesoap.server import SoapDispatcher, WSGISOAPHandler
from http.server import BaseHTTPRequestHandler, HTTPServer
import re

# método com a implementação da operação/serviço
def is_par(in0):
    return in0 % 2 == 0

def is_mathOp(operador, num1, num2):
    if(operador == "+"):
        return num1 + num2

    elif(operador == "-"):
        return num1 - num2

    elif(operador == "*"):
        return num1 * num2

    elif(operador == "/"):
        return num1 / num2
    
    else:
        return "Operador inválido, tente novamente!!"

def isCpfValid(cpf):

    if not isinstance(cpf,str):
        return False

    cpf = re.sub("[^0-9]",'',cpf)

    if cpf=='00000000000' or cpf=='11111111111' or cpf=='22222222222' or cpf=='33333333333' or cpf=='44444444444' or cpf=='55555555555' or cpf=='66666666666' or cpf=='77777777777' or cpf=='88888888888' or cpf=='99999999999':
        return False

    if len(cpf) != 11:
        return False

    sum = 0
    weight = 10

    for n in range(9):
        sum = sum + int(cpf[n]) * weight

        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        firstVerifyingDigit = 0
    else:
        firstVerifyingDigit = verifyingDigit

    sum = 0
    weight = 11
    for n in range(10):
        sum = sum + int(cpf[n]) * weight

        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        secondVerifyingDigit = 0
    else:
        secondVerifyingDigit = verifyingDigit

    if cpf[-2:] == "%s%s" % (firstVerifyingDigit,secondVerifyingDigit):
        return True
    return False

#criação do objeto soap
dispatcher = SoapDispatcher('AbcBolinhas',
location='http://localhost:8888/',action='http://localhost:8888/',namespace="http://localhost:8888/",
prefix="ns0", documentation="Exemplo usando SOAP através de PySimpleSoap",
trace=True, debug=True,ns=True)

# publicação do serviço, com seu alias, retorno e parâmetros
dispatcher.register_function('verifica_NumeroPar', is_par, returns={'out2': bool}, args={'in0': int})
dispatcher.register_function('valida_CPF', isCpfValid, returns={'out0': bool}, args={'cpf': str})
dispatcher.register_function('math_operation', is_mathOp, returns={'out1': str}, args={'operador': str, 'num1' : int, 'num2' : int})

class SOAPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """User viewable help information and wsdl"""
        args = self.path[1:].split("?")
        if self.path != "/" and args[0] not in self.server.dispatcher.methods.keys():
            self.send_error(404, "Method not found: %s" % args[0])
        else:
            if self.path == "/":
                # return wsdl if no method supplied
                response = self.server.dispatcher.wsdl()
            else:
                # return supplied method help (?request or ?response messages)
                req, res, doc = self.server.dispatcher.help(args[0])
                if len(args) == 1 or args[1] == "request":
                    response = req
                else:
                    response = res
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.end_headers()
            self.wfile.write(response)

    def do_POST(self):
        """SOAP POST gateway"""
        request = self.rfile.read(int(self.headers.get('content-length')))
        # convert xml request to unicode (according to request headers)
        encoding = self.headers.get_param("charset")
        request = request.decode(encoding)
        fault = {}
        # execute the method
        response = self.server.dispatcher.dispatch(request, fault=fault)
        # check if fault dict was completed (faultcode, faultstring, detail)
        if fault:
            self.send_response(500)
        else:
            self.send_response(200)
        self.send_header("Content-type", "text/xml")
        self.end_headers()
        self.wfile.write(response)

def main():
    httpd = HTTPServer(("", 8888), SOAPHandler)
    httpd.dispatcher = dispatcher
    httpd.serve_forever()

if __name__ == '__main__':
    main()