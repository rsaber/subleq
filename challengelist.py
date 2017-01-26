challenges = [
{
        'id' : 1,
        'text' : 'Your first challenge is to write a program that adds two numbers together. The input is at address 50 and 51 and the result must be stored at address 50',
        'tests' : [
            # Test Case
            [
                # Test Inputs [a,b] means store a in b
                [[7,50],[8,51]],
                # Test Outputs [a,b] means check if val at b == a
                [[15,50]]
            ],
            [
                # Test Inputs [a,b] means store a in b
                [[100,50],[-8,51]],
                # Test Outputs [a,b] means check if val at b == a
                [[92,50]]
            ],
        ]
},
{
        'id' : 2,
        'text' : 'Write a program that multiplies two numbers together. The inputs will be stored in address 60 and 61, store the final result 16 bit result in 62,63',
        'tests' : [
            # Test Case
            [
                # Test Inputs [a,b] means store a in b
                [[7,50],[8,51]],
                # Test Outputs [a,b] means check if val at b == a
                [[15,50]]
            ]
        ]
},
]
