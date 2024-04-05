@if "%ECHOON%" == "" (@echo off) else (@echo %ECHOON%)&:: set ECHOON=on if you want to debug this script
@::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@::  THIS FILE IS 100% GENERATED BY ZPROJECT; DO NOT EDIT EXCEPT EXPERIMENTALLY  ::
@::  Read the zproject/README.md for information about making permanent changes. ::
@::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@setlocal
:-  configure.bat creates platform.h and configures the build process
:-  You MUST run this before building via msbuild or VisualStudio.

IF %1.==--help. (
    ECHO Syntax: configure [ switch ]
    ECHO    --help                  show this help
    ECHO    --enable-drafts         from zip package, enables DRAFT API
    ECHO    --disable-drafts        from git repository, disables DRAFT API
    ECHO    --without-filemq_server  do not build filemq_server.exe
    ECHO    --without-filemq_client  do not build filemq_client.exe
    ECHO    --without-filemq_selftest  do not build filemq_selftest.exe
    GOTO :eof
)
ECHO Configuring filemq...

:- make sure our directory is builds\msvc no matter where user is when executing it from
@pushd %~dp0%

ECHO //  Generated by configure.bat> platform.h
ECHO. >> platform.h
ECHO #ifndef __PLATFORM_H_INCLUDED__>> platform.h
ECHO #define __PLATFORM_H_INCLUDED__>> platform.h
ECHO. >> platform.h
ECHO #define FILEMQ_HAVE_WINDOWS 1>> platform.h

:-  Check for dependencies
IF EXIST "..\..\..\libzmq" (
    ECHO Building with libzmq
    ECHO #define HAVE_LIBZMQ 1>> platform.h
) ELSE (
    ECHO Building without libzmq
    ECHO filemq cannot build without libzmq
    ECHO Please clone https://github.com/zeromq/libzmq.git, and then configure ^& build
    ECHO TODO: resolve this problem automatically.
    GOTO error
)
IF EXIST "..\..\..\czmq" (
    ECHO Building with czmq
    ECHO #define HAVE_CZMQ 1>> platform.h
) ELSE (
    ECHO Building without czmq
    ECHO filemq cannot build without czmq
    ECHO Please clone https://github.com/zeromq/czmq.git, and then configure ^& build
    ECHO TODO: resolve this problem automatically.
    GOTO error
)

:-  Check if we want to build the draft API
if "%1" == "--enable-drafts" goto :with_draft
if "%1" == "--disable-drafts" goto :no_draft
IF NOT EXIST "..\..\.git" GOTO no_draft
:with_draft
    ECHO Building with draft API (stable + legacy + draft API)
    ECHO //  Provide draft classes and methods>>platform.h
    ECHO #define FILEMQ_BUILD_DRAFT_API 1>>platform.h
    GOTO end_draft
:no_draft
    ECHO Building without draft API (stable + legacy API)
    ECHO #undef FILEMQ_BUILD_DRAFT_API 1>>platform.h
:end_draft
ECHO. >> platform.h
ECHO #endif>> platform.h
goto :done

:done
popd
@endlocal
:: this is how you code a return in a windows batch script... "goto :eof"
:: you see after a "call :label", %0 == ":label" inside :label, until "goto :eof" happens.
@if "%0:~1,1" == ":" @goto :eof
@exit /b 0

:error
call :done
@exit /b 1
