#include <Python.h>
#include "adapters/include/client/exceptions.h"
#include "adapters/include/client/config.h"


PyObject *FailedConnection = NULL;

void init_exceptions(void) {
    PyObject *exceptions_module = PyImport_ImportModule(ZCLIENT_MODULE_NAME ".exceptions");
    if (!exceptions_module) {
        return;
    }

    FailedConnection = PyObject_GetAttrString(exceptions_module, "FailedConnection");


    // Done with the module
    Py_DECREF(exceptions_module);

    // Validate all
    if (!FailedConnection)
        PyErr_SetString(PyExc_ImportError, "Failed to initialize custom exceptions");
}
