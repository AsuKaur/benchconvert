#include "verifier_functions.h"

void entry(const float tensor_onnx__Gemm_0[1][2], float tensor_7[1][2]);

int main()
{
	float tensor_onnx__Gemm_0[1][2];
	float tensor_7[1][2];

	tensor_onnx__Gemm_0[0][0] = __VERIFIER_nondet_float();
	tensor_onnx__Gemm_0[0][1] = __VERIFIER_nondet_float();

	__VERIFIER_assume(tensor_onnx__Gemm_0[0][0] >= 0.0f && tensor_onnx__Gemm_0[0][0] <= 1.0f);
	__VERIFIER_assume(tensor_onnx__Gemm_0[0][1] >= 0.0f && tensor_onnx__Gemm_0[0][1] <= 1.0f);

	entry(tensor_onnx__Gemm_0, tensor_7);

	// Expected result: SAT - assertion should always hold
	__VERIFIER_assert(!(tensor_7[0][0] >= 1.0f && tensor_7[0][1] <= 0.0f));

	return 0;
}


