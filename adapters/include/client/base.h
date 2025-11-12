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

PyObject *
run_make_client_request(PyObject* self, PyObject* args, PyObject* kwargs);

PyObject *
run_listen_client_input(PyObject* self, PyObject* args, PyObject* kwargs);

PyObject *
run_process_client_input(PyObject* self, PyObject* args, PyObject* kwargs);

PyObject *
run_get_client_response(PyObject* self, PyObject* args, PyObject* kwargs);

PyObject *
run_pop_client_unrequested_payload(PyObject* self, PyObject* args, PyObject* kwargs);

PyObject *
run_is_client_connected(PyObject* self, PyObject* args, PyObject* kwargs);


#endif
