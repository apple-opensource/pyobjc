/*
 * This module is used in the unittests for object initialize.
 */
#include "Python.h"
#include "pyobjc-api.h"

#import <Foundation/Foundation.h>


static PyMethodDef mod_methods[] = {
	{ 0, 0, 0, 0 }
};

typedef struct TestStructPointerStruct* Foo;

#if PY_VERSION_HEX >= 0x03000000

static struct PyModuleDef mod_module = {
	PyModuleDef_HEAD_INIT,
	"structpointer2",
	NULL,
	0,
	mod_methods,
	NULL,
	NULL,
	NULL,
	NULL
};

#define INITERROR() return NULL
#define INITDONE() return m

PyObject* PyInit_structpointer2(void);

PyObject*
PyInit_structpointer2(void)

#else

#define INITERROR() return
#define INITDONE() return

void initstructpointer2(void);

void
initstructpointer2(void)
#endif
{
	PyObject* m;
	PyObject* v;

#if PY_VERSION_HEX >= 0x03000000
	m = PyModule_Create(&mod_module);
#else
	m = Py_InitModule4("structpointer2", mod_methods,
		NULL, NULL, PYTHON_API_VERSION);
#endif
	if (!m) {
		INITERROR();
	}

	if (PyObjC_ImportAPI(m) < 0) {
		INITERROR();
	}
	v = PyObjCCreateOpaquePointerType("TestStructPointerStructPtr",
			@encode(Foo), NULL);
	if (v == NULL) {
		INITERROR();
	}
	if (PyDict_SetItemString(PyModule_GetDict(m), "TestStructPointerStructPtr",
			v) < 0) {
		INITERROR();
	}

	INITDONE();
}
