# Degrad Pseudo Code

## CSSTFN (N:1-5 )
* Stores event data for N-th generation fluorescence
* Need to do globls for this 

## CALCNE (N:1-5)
* Using initial energy deposit and shell vacancy created at ISHELL :
	* Calculate Cascade in gas KGAS
	* Calculate Cascade in molecular component LGAS
* Stores photoelectron energy and angle 
* Get THET from ANGGEN function 
* Get DRXX,DRYY,DRZZ from DRCOS()
* Loop around cascade
	* Calculate energy of electron 
	* Stop if ion charge state > 28
	* Get a random emission angle 
	* Update()
		* Normalize
		* Save photon energy 
		* Random R3 and R4 
		* Find lowest vacancy 

## DRCOS
* Given direction Cosines and scattering by angle(theta,phi) 
* Calculate new direction cosines 

## ANGGEN
* Generate a random number y
* Do a Monte Carlo to return a converged theta

## SPLITN (N:1-5)
* SPLIT1 find a legitimate WPL and hence ESEC

