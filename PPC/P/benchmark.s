	.file	"benchmark.cc"
	.text
	.section	.rodata
	.type	_ZStL19piecewise_construct, @object
	.size	_ZStL19piecewise_construct, 1
_ZStL19piecewise_construct:
	.zero	1
	.local	_ZStL8__ioinit
	.comm	_ZStL8__ioinit,1,1
	.text
	.globl	_Z5rdtscv
	.type	_Z5rdtscv, @function
_Z5rdtscv:
.LFB1522:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
#APP
# 7 "benchmark.cc" 1
	rdtsc
# 0 "" 2
#NO_APP
	movl	%eax, -8(%rbp)
	movl	%edx, -4(%rbp)
	movl	-4(%rbp), %eax
	salq	$32, %rax
	movq	%rax, %rdx
	movl	-8(%rbp), %eax
	orq	%rdx, %rax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1522:
	.size	_Z5rdtscv, .-_Z5rdtscv
	.section	.rodata
.LC3:
	.string	"Number of clock cycles: %ld\n"
	.align 8
.LC5:
	.string	"The program took %f seconds of wall time\n"
	.align 8
.LC6:
	.string	"The program took %f seconds of cpu time\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB1523:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$160, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movss	.LC0(%rip), %xmm0
	movss	%xmm0, -152(%rbp)
	movss	.LC1(%rip), %xmm0
	movss	%xmm0, -148(%rbp)
	pxor	%xmm0, %xmm0
	movss	%xmm0, -160(%rbp)
	call	_Z5rdtscv
	movq	%rax, -144(%rbp)
	leaq	-80(%rbp), %rax
	movq	%rax, %rsi
	movl	$0, %edi
	call	clock_gettime@PLT
	leaq	-48(%rbp), %rax
	movq	%rax, %rsi
	movl	$2, %edi
	call	clock_gettime@PLT
#APP
# 24 "benchmark.cc" 1
	############LOOP############
# 0 "" 2
#NO_APP
	movl	$0, -156(%rbp)
.L5:
	cmpl	$999999999, -156(%rbp)
	jg	.L4
	movss	-152(%rbp), %xmm0
	movaps	%xmm0, %xmm1
	subss	-148(%rbp), %xmm1
	movss	-152(%rbp), %xmm0
	addss	-148(%rbp), %xmm0
	mulss	%xmm1, %xmm0
	movaps	%xmm0, %xmm2
	addss	-160(%rbp), %xmm2
	movss	-152(%rbp), %xmm0
	addss	-148(%rbp), %xmm0
	movss	-152(%rbp), %xmm1
	subss	-148(%rbp), %xmm1
	divss	%xmm1, %xmm0
	addss	%xmm2, %xmm0
	movss	%xmm0, -160(%rbp)
	addl	$1, -156(%rbp)
	jmp	.L5
.L4:
	call	_Z5rdtscv
	subq	-144(%rbp), %rax
	movq	%rax, -136(%rbp)
	movq	-136(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC3(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-64(%rbp), %rax
	movq	%rax, %rsi
	movl	$0, %edi
	call	clock_gettime@PLT
	leaq	-32(%rbp), %rax
	movq	%rax, %rsi
	movl	$2, %edi
	call	clock_gettime@PLT
	movq	-64(%rbp), %rdx
	movq	-80(%rbp), %rax
	subq	%rax, %rdx
	movq	%rdx, %rax
	movq	%rax, -128(%rbp)
	movq	-32(%rbp), %rdx
	movq	-48(%rbp), %rax
	subq	%rax, %rdx
	movq	%rdx, %rax
	movq	%rax, -120(%rbp)
	movq	-56(%rbp), %rdx
	movq	-72(%rbp), %rax
	subq	%rax, %rdx
	movq	%rdx, %rax
	movq	%rax, -112(%rbp)
	movq	-24(%rbp), %rdx
	movq	-40(%rbp), %rax
	subq	%rax, %rdx
	movq	%rdx, %rax
	movq	%rax, -104(%rbp)
	cvtsi2sdq	-128(%rbp), %xmm1
	cvtsi2sdq	-112(%rbp), %xmm2
	movsd	.LC4(%rip), %xmm0
	mulsd	%xmm2, %xmm0
	addsd	%xmm1, %xmm0
	movsd	%xmm0, -96(%rbp)
	cvtsi2sdq	-120(%rbp), %xmm1
	cvtsi2sdq	-104(%rbp), %xmm2
	movsd	.LC4(%rip), %xmm0
	mulsd	%xmm2, %xmm0
	addsd	%xmm1, %xmm0
	movsd	%xmm0, -88(%rbp)
	movq	-96(%rbp), %rax
	movq	%rax, %xmm0
	leaq	.LC5(%rip), %rdi
	movl	$1, %eax
	call	printf@PLT
	movq	-88(%rbp), %rax
	movq	%rax, %xmm0
	leaq	.LC6(%rip), %rdi
	movl	$1, %eax
	call	printf@PLT
	movl	$0, %eax
	movq	-8(%rbp), %rcx
	xorq	%fs:40, %rcx
	je	.L7
	call	__stack_chk_fail@PLT
.L7:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1523:
	.size	main, .-main
	.type	_Z41__static_initialization_and_destruction_0ii, @function
_Z41__static_initialization_and_destruction_0ii:
.LFB2004:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	cmpl	$1, -4(%rbp)
	jne	.L10
	cmpl	$65535, -8(%rbp)
	jne	.L10
	leaq	_ZStL8__ioinit(%rip), %rdi
	call	_ZNSt8ios_base4InitC1Ev@PLT
	leaq	__dso_handle(%rip), %rdx
	leaq	_ZStL8__ioinit(%rip), %rsi
	movq	_ZNSt8ios_base4InitD1Ev@GOTPCREL(%rip), %rax
	movq	%rax, %rdi
	call	__cxa_atexit@PLT
.L10:
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2004:
	.size	_Z41__static_initialization_and_destruction_0ii, .-_Z41__static_initialization_and_destruction_0ii
	.type	_GLOBAL__sub_I__Z5rdtscv, @function
_GLOBAL__sub_I__Z5rdtscv:
.LFB2005:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	$65535, %esi
	movl	$1, %edi
	call	_Z41__static_initialization_and_destruction_0ii
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2005:
	.size	_GLOBAL__sub_I__Z5rdtscv, .-_GLOBAL__sub_I__Z5rdtscv
	.section	.init_array,"aw"
	.align 8
	.quad	_GLOBAL__sub_I__Z5rdtscv
	.section	.rodata
	.align 4
.LC0:
	.long	1066192077
	.align 4
.LC1:
	.long	1067030938
	.align 8
.LC4:
	.long	3894859413
	.long	1041313291
	.hidden	__dso_handle
	.ident	"GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
