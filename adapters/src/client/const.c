#include "adapters/include/client/const.h"
#include "core/include/common/methods.h"


void init_methods(PyObject *m) {
    if (!m) return;

    for (int i = 0; i < METHODS_COUNT; ++i) {
        PyModule_AddIntConstant(m, methods_str[i], i);
    }
}
