#ifndef ZCLIENT_ADAPTER_EXCEPTIONS_H
#define ZCLIENT_ADAPTER_EXCEPTIONS_H

#include <Python.h>


extern PyObject *FailedConnection;


void init_exceptions();

#endif
