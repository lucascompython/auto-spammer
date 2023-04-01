cython --embed -3 main.py

call "%ProgramFiles%\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64

cl main.c /MD /I "C:\Users\lucas\AppData\Local\Programs\Python\Python311\include" /link "C:\Users\lucas\AppData\Local\Programs\Python\Python311\libs\python311.lib"  "%WindowsSdkDir%Lib\%WindowsSDKVersion%um\%VSCMD_ARG_HOST_ARCH%\User32.lib" "%WindowsSdkDir%Lib\%WindowsSDKVersion%um\%VSCMD_ARG_HOST_ARCH%\Kernel32.lib"
