#ifndef ZCLIENT_ADAPTER_BASE_H
#define ZCLIENT_ADAPTER_BASE_H

#include <Python.h>

#define ZHANDLER_NAME_STR "zclient_handler_t"

PyObject *
run_create_client(PyObject* self, PyObject* args, PyObject* kwargs);

PyObject *
run_destroy_client(PyObject* self, PyObject* args, PyObject* kwargs);

PyObject *
run_connect_client(PyObject* self, PyObject* args, PyObject* kwargs);

PyObject *
run_disconnect_client(PyObject* self, PyObject* args, PyObject* kwargs);



#endif
