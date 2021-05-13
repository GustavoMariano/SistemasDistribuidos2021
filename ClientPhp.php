<?php
	$wsdl   = 'http://localhost:8888/';
	$client = new SoapClient($wsdl, array('trace'=>1));  // The trace param will show you errors
	
//--------------------------------------------------------------------------------------------------------

	$input_numero = 11;

	$request_param = array(
	'in0' => $input_numero
	);

	try {
		$responce_param = $client->verifica_NumeroPar($request_param);
		$resultadoPar = $responce_param->out2;
        if($resultadoPar == null){
            echo 'false';
        }
        else{
            echo 'true';
        }
	} catch (Exception $e) {
		echo "<h2>Exception Error</h2>";
		echo $e->getMessage();
	}
	
//--------------------------------------------------------------------------------------------------------
	
	$input_operador = '+';
	$input_numero1 = 11;
	$input_numero2 = 10;

	$request_param = array(
	'operador' => $input_operador, 'num1' => $input_numero1, 'num2' => $input_numero2
	);

	try {
		$responce_param = $client->math_operation($request_param);
		echo $responce_param->out1;
	} catch (Exception $e) {
		echo "<h2>Exception Error</h2>";
		echo $e->getMessage();
	}
	
//--------------------------------------------------------------------------------------------------------
	
	$input_cpf = '11111111111';

	$request_param = array(
	'cpf' => $input_cpf
	);

	try {
		$responce_param = $client->valida_CPF($request_param);
		$resultado = $responce_param->out0;
		if($resultado == null){
			echo 'false';
		}
		else{
			echo 'true';
		}
		
	} catch (Exception $e) {
		echo "<h2>Exception Error</h2>";
		echo $e->getMessage();
	}
			
?>  