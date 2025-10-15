#include "adapters/include/client/const.h"
#include "core/include/common/methods.h"


void init_methods(PyObject *m) {
    if (!m) return;

    PyObject *methods_dict = PyDict_New();
    if (!methods_dict) return;

    for (int i = 0; i < METHODS_COUNT; ++i) {
        PyObject *val = PyLong_FromLong(i);
        if (!val) {
            Py_DECREF(methods_dict);
            return;
        }
        PyDict_SetItemString(methods_dict, methods_str[i], val);
        Py_DECREF(val);
    }

    PyModule_AddObject(m, "METHODS", methods_dict);
}
