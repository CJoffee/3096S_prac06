/* Registers
@ r2	offset for accessing address 4 bytes apart
@ r7 return register
@ lr Link register
@ r4	Loop variable, _i_					R4
@ r5	Address of head of list					R5
@ r6	Size of _List_						R6
@ r8	Comparison variable, _value_				R8
@ r9	List item being compared (List[i])			R9
@ r10	Address of List[i+1] (value in each loop/$t3)		R10
@ r11	Address of List[i] (comparative list item/$t4)		R11
@ r12	For Loop variable to count number of loops:		R12
*/
.data
array:	.space 64	@ 16 integers, 4 bytes each

.text
mov r4, #1 	/*Load 1 into r4*/
mov r12, #1	/*Load 1 into r12*/
ldr r5, =array	/*Load Address of List head into r5*/
mov r6, #16	/*Load List length into r6*/

loop_list:
	mov r4, r12	/*Copy r12 to r4*/
	mul r2, r4, #4	/*4 bytes per list item*/
	add r10, r5, r2	/*Load Address of List[r4] into r10*/
	ldr r8, [r10]	/*Load value at [r10] into r8*/
	sub r4, r4, #1	/*Subtract 1 from r4*/
	b while_gt0	/*branch while_gt0*/

while_gt0:
	mul r2, r4, #4			/*4 bytes per list item*/
	add r11, r5, r2			/*Load Address of List[r4] into r11*/
	ldr r9, [r11]			/*Load value at [r11] into r9*/
	blt r8, r9, b less_than		/*If r8 < r9, branch less_than:*/
	b next_for			/*branch next_for:*/

less_than:
	str r9, [r10]			/*Store r9 in [r10]*/
	str r8, [r11]			/*Store r8 in [r11]*/
	sub r4, r4, #1			/*Subtract 1 from r4*/
	blt r4, #0, b next_for		/*If r4 < 0, branch next_for*/
	b while_gt0			/*branch while_gt0*/

next_for:
	add r12, r12, #1	/*Add 1 to r12*/
	bgt r12, r6, b exit	/*if r12 > r6, branch exit*/
	b loop_list		/*branch loop_list*/
exit:
	/*mov r0, r4*/		/*Copy r4 to return register*/
	ldr lr, [r5]		/*Return sorted array register*/
	bx lr			/*Exit/Shutdown program*/
