#include <Python.h>
#include "adapters/include/client/base.h"
#include "adapters/include/client/classes.h"
#include "adapters/include/client/exceptions.h"
#include "adapters/include/client/const.h"


static PyMethodDef AdapterMethods[] = {
    {"_create_client",
     run_create_client,
     METH_VARARGS | METH_KEYWORDS,
     "Initialize Zeitgeist client as `zclient_handler_t`"},
    {"_destroy_client",
     run_destroy_client,
     METH_VARARGS | METH_KEYWORDS,
     "Destroy `zclient_handler_t`"},
    {"_connect_client",
     run_connect_client,
     METH_VARARGS | METH_KEYWORDS,
     "Connect `zclient_handler_t`"},
    {"_disconnect_client",
     run_disconnect_client,
     METH_VARARGS | METH_KEYWORDS,
     "Disconnect `zclient_handler_t`"},
    {"_make_client_request",
     run_make_client_request,
     METH_VARARGS | METH_KEYWORDS,
     "Make `zclient_handler_t` request"},
    {"_listen_client_input",
     run_listen_client_input,
     METH_VARARGS | METH_KEYWORDS,
     "Listen to `zclient_handler_t` input"},
    {"_process_client_input",
     run_process_client_input,
     METH_VARARGS | METH_KEYWORDS,
     "Process `zclient_handler_t` input"},
    {"_get_client_response",
     run_get_client_response,
     METH_VARARGS | METH_KEYWORDS,
     "Get `zclient_handler_t` response"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef adaptermodule = {
    PyModuleDef_HEAD_INIT,
    "_adapter",
    "Zeitgeist C client adapter",
    -1,
    AdapterMethods,
    NULL,  // m_slots
    NULL,  // m_traverse
    NULL,  // m_clear
    NULL   // m_free
};

PyMODINIT_FUNC PyInit__adapter(void) {
    PyObject *m = PyModule_Create(&adaptermodule);
    if (!m)
        return (NULL);

    init_exceptions();
    init_classes();
    init_methods(m);

    return (m);
}
