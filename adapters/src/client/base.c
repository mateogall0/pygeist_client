#include "adapters/include/client/base.h"
#include "core/include/client/master.h"
#include "core/include/common/methods.h"
#include "adapters/include/client/exceptions.h"
#include "adapters/include/client/config.h"
#include "adapters/include/client/classes.h"


PyObject*
run_create_client(PyObject* self,
                  PyObject* args,
                  PyObject* kwargs) {
    (void)self;
    size_t upc = 1;
    size_t rpc = 1;

    static char *kwlist[] = {"upc", "rpc", NULL};

    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "|nn",
                                     kwlist,
                                     &upc,
                                     &rpc))
        return (NULL);
    zclient_handler_t* zclient = create_zclient(upc, rpc);
    if (!zclient)
        return (PyErr_NoMemory());

    return (PyCapsule_New(zclient,
                          ZHANDLER_NAME_STR,
                          NULL));
}

PyObject *
run_destroy_client(PyObject* self, PyObject* args, PyObject* kwargs) {
    (void)self;
    PyObject* capsule;
    static char *kwlist[] = {"zclient_handler", NULL};

    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "O",
                                     kwlist,
                                     &capsule))
        return (NULL);

    zclient_handler_t* zclient = PyCapsule_GetPointer(capsule, ZHANDLER_NAME_STR);
    if (!zclient)
        return (NULL);
    destroy_zclient(zclient);
    Py_RETURN_NONE;
}

PyObject *
run_connect_client(PyObject* self, PyObject* args, PyObject* kwargs) {
    (void)self;
    PyObject* capsule;
    static char *kwlist[] = {"zclient_handler", "url", "port", NULL};
    char *url;
    int32_t port;

    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "Osi",
                                     kwlist,
                                     &capsule,
                                     &url,
                                     &port))
        return (NULL);

    zclient_handler_t* zclient = PyCapsule_GetPointer(capsule, ZHANDLER_NAME_STR);
    if (!zclient)
        return (NULL);
    if (connect_zclient(zclient, url, port) == 1) {
        PyErr_SetString(FailedConnection,
                        "couldn't connect");

        return (NULL);
    }
    Py_RETURN_NONE;
}

PyObject *
run_disconnect_client(PyObject* self, PyObject* args, PyObject* kwargs) {
    (void)self;
    PyObject* capsule;
    static char *kwlist[] = {"zclient_handler", NULL};

    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "O",
                                     kwlist,
                                     &capsule))
        return (NULL);

    zclient_handler_t* zclient = PyCapsule_GetPointer(capsule, ZHANDLER_NAME_STR);
    if (!zclient)
        return (NULL);
    disconnect_zclient(zclient);
    Py_RETURN_NONE;
}

PyObject *
run_make_client_request(PyObject* self, PyObject* args, PyObject* kwargs) {
    (void)self;
    static char *kwlist[] = {"zclient_handler",
                             "method",
                             "target",
                             "headers",
                             "body",
                             NULL};
    PyObject* capsule;
    int method = 0;
    char *target = "";
    char *headers = "";
    char *body = "";

    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "Ois|ss",
                                     kwlist,
                                     &capsule,
                                     &method,
                                     &headers,
                                     &body))
        return (NULL);

    zclient_handler_t* zclient = PyCapsule_GetPointer(capsule, ZHANDLER_NAME_STR);
    if (!zclient)
        return (NULL);

    unsigned long req_id = zclient_make_request(zclient, method, target, headers, body);

    return PyLong_FromUnsignedLong(req_id);
}

PyObject *
run_listen_client_input(PyObject* self, PyObject* args, PyObject* kwargs) {
    (void)self;
    static char *kwlist[] = {"zclient_handler", NULL};
    PyObject* capsule;

    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "O",
                                     kwlist,
                                     &capsule))
        return (NULL);

    zclient_handler_t* zclient = PyCapsule_GetPointer(capsule, ZHANDLER_NAME_STR);
    if (!zclient)
        return (NULL);
    zclient_listen_input(zclient);

    Py_RETURN_NONE;
}

PyObject *
run_process_client_input(PyObject* self, PyObject* args, PyObject* kwargs) {
    (void)self;
    static char *kwlist[] = {"zclient_handler", NULL};
    PyObject* capsule;

    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "O",
                                     kwlist,
                                     &capsule))
        return (NULL);

    zclient_handler_t* zclient = PyCapsule_GetPointer(capsule, ZHANDLER_NAME_STR);
    if (!zclient)
        return (NULL);
    zclient_process_input(zclient);

    Py_RETURN_NONE;
}

PyObject *
run_get_client_response(PyObject* self, PyObject* args, PyObject* kwargs) {
    (void)self;
    static char *kwlist[] = {"zclient_handler", "req_id", NULL};
    PyObject* capsule;
    unsigned long req_id;

    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "Ok",
                                     kwlist,
                                     &capsule,
                                     &req_id))
        return (NULL);
    zclient_handler_t* zclient = PyCapsule_GetPointer(capsule, ZHANDLER_NAME_STR);
    if (!zclient)
        return (NULL);

    zclient_response_t *res = zclient_get_response(zclient, req_id);
    if (!res) {
        PyErr_SetString(FailedResponseProcess,
                        "response not found");
        return (NULL);
    }
    PyObject* arglist = Py_BuildValue("(ksss)",
                                      res->id,
                                      res->headers,
                                      res->body,
                                      res->status_msg);
    PyObject* instance = PyObject_CallObject(Response, arglist);

    Py_DECREF(arglist);

    return (instance);
}

PyObject *
run_pop_client_unrequested_payload(PyObject* self, PyObject* args, PyObject* kwargs) {
    (void)self;
    static char *kwlist[] = {"zclient_handler", NULL};
    PyObject* capsule;

    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "O",
                                     kwlist,
                                     &capsule))
        return (NULL);
    zclient_handler_t* zclient = PyCapsule_GetPointer(capsule, ZHANDLER_NAME_STR);
    if (!zclient)
        return (NULL);
    received_payload_t *payload = zclient_pop_unrequested_payload(zclient);
    PyObject* arglist = Py_BuildValue("(s)", payload->data);
    PyObject* instance = PyObject_CallObject(Unrequested, arglist);
    Py_DECREF(arglist);

    return (instance);

}
