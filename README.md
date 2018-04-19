# GasSimulator 
The aim of this repo is to build a tool and a semi-automated algorithm, to convert FORTRAN code to python<br>

<h2> RECENT </h2><br>
Added f2py interface example code in testing directory. Code file -> ftype .
Terminal Screenshot -> Screenshot <br>

magboltz.py is the lastest conversion <br>

<b>Features of change.py currently :</b> <br>
1.map arithematical operators from FORTRAN to corresponding in python <br>
2.map logical operators from FORTRAN to corresponsing operators in python <br>
3.retain comments as comments<br>
4.map dabs,dsqrt,dlog,dexp functions correctly<br>
5.replace FORTRAN do to Python for-loop<br>
6.replace irrelevant conditions like endif <br>
7.add : after function definition<br>
8.remove datatype declarations<br>

<h2> Installing F2Py</h2><br>
cd testing/F2PY-2.45.241_1926<br>
sudo python setup.py install<br>
cd ../scipy_distutils-0.3.3_34.586<br>
sudo python setup.py install<br>

