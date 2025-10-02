#include "adapters/include/client/classes.h"
#include "adapters/include/client/config.h"


PyObject *Response = NULL;


void init_classes() {
    PyObject *response_module = PyImport_ImportModule(ZCLIENT_MODULE_NAME ".response");
    if (!response_module)
        return;

    Response = PyObject_GetAttrString(response_module, "Response");

    Py_DECREF(response_module);

    // Validate all
    if (!Response)
        PyErr_SetString(PyExc_ImportError,
                        "failed to initialize classes");
}
