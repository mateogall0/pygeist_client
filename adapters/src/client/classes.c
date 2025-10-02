#include "adapters/include/client/classes.h"
#include "adapters/include/client/config.h"


PyObject *Response = NULL;
PyObject *Unrequested = NULL;


void init_classes() {
    PyObject *response_module = PyImport_ImportModule(ZCLIENT_MODULE_NAME
                                                      ".response");
    PyObject *unrequested_module = PyImport_ImportModule(ZCLIENT_MODULE_NAME
                                                         ".unrequested");
    if (!response_module ||
        !unrequested_module)
        return;

    Response = PyObject_GetAttrString(response_module, "Response");
    Unrequested = PyObject_GetAttrString(unrequested_module, "Unrequested");

    Py_DECREF(response_module);
    Py_DECREF(unrequested_module);


    // Validate all
    if (!Response ||
        !Unrequested)
        PyErr_SetString(PyExc_ImportError,
                        "failed to initialize classes");
}
