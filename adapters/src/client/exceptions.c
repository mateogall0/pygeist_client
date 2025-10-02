#include <Python.h>
#include "adapters/include/client/exceptions.h"
#include "adapters/include/client/config.h"


PyObject *FailedConnection = NULL;
PyObject *NotConnected = NULL;
PyObject *FailedResponseProcess = NULL;

void init_exceptions(void) {
    PyObject *exceptions_module = PyImport_ImportModule(ZCLIENT_MODULE_NAME ".exceptions");
    if (!exceptions_module)
        return;

    FailedConnection = PyObject_GetAttrString(exceptions_module, "FailedConnection");
    NotConnected = PyObject_GetAttrString(exceptions_module, "NotConnected");
    FailedResponseProcess = PyObject_GetAttrString(exceptions_module, "FailedResponseProcess");


    // Done with the module
    Py_DECREF(exceptions_module);

    // Validate all
    if (!FailedConnection ||
        !NotConnected ||
        !FailedResponseProcess)
        PyErr_SetString(PyExc_ImportError,
                        "failed to initialize custom exceptions");
}
