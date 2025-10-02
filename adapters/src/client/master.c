#include <Python.h>
#include "adapters/include/client/base.h"
#include "adapters/include/client/exceptions.h"


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

    return (m);
}
