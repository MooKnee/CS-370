To run the prgoram, run it with following specifications:
Input:
    The values of parameters stepSize, epsilon and M will be given in command line arguments, as specified below.
    Another command line argument will be the number of iterations of random restart to run.
Command Line Arguments:
    Your program classify should take five or six command line arguments, in sequence:
        -the name of the file for the training set;
        -the values of:
            stepSize,
            epsilon and
            M;
        -the number of random restarts, and,
        -optionally “-v” to indicate verbose output.
            -(The -v is optional when running your program, but it is mandatory to add support for it as a part of the assignment).
            For example in python, the command to execute my program might be: python3 Mooney-Caitlin-A3.py training.csv 0.1 0.01 0.2 100 -v
Note:
The file may be wonky

Notes:
Terms:
- A_1_, ..., A_k_
    - are numeric predictive attributes
- CE
    - classification attribute, is discrete, with 2 or more values
- dom(C)
    - set of possible values of the classification attribute
- X
    - instance
- u(X)
    - vector of predictive attributes
- T
    - training set
- v
    - element of dom(C)
- T_v_
    - set of instances X ∈ T (X element in T), where X.C = v; For each value v of the classification attribute, compute the centroid
- centeroid
    - formula g_v_ = [1/(|T_v_|)] * Σ _(Y ∈ T_v_)_ [u(Y)]
- g_v_
    - vectors, are output of the learning stage
- Z
    - new instance
- exemplar vectors
    - assume no two exemplar vectors are equal
- Euclidean Distance
    - distance, instead find distance squared and minimize that
- distance squared and minimized
    - formula v = argmin_w ∈ dom(C)_ d^_2_(~g_w_ , ~u(Z))
    - where d^_2_(x,y) = kSum_i=1_ (x_i - y_i)^_2_
- exemplar points
    - choice of exemplar points minimizes the objective function
- objective function
    - sum of the distance squared from each data point in the training set to the exemplar of its category.
    - formula O_T_(g_1_, ..., g_c_) = Σ_v ϵ dom(T)_ Σ_z ϵ T_v__d^_2_(g_v_,z)

- test point
    - The classifier classifies a test point according to the closest exemplar vector
- N
    - number of instances in the training set
- k
    - number of predictive attributes
- c
    - number of different values of the classification attribute

- uses same classifier
- c
    - set of exemplar vectors; learning algorithm produces a set of c exemplar vectors (used during classification phase)
- objective function
    - modify  to charge a “cost” only to misclassified points
- G
    -  a tuple of exemplar vectors G = {~g_1_ , ..., ~g_c_ }
- Y
    - given training example
- Y.C
    - Y.C = v
- r_G_(Y)
    -  the closest exemplar vector to Y (assume there are no ties)
    - if r_G_ = g_v_, then G is correctly classifying Y
    - formula d^_2_(g_v_,u(Y)) - d^_2_(r_G_(Y),u(Y)) is zero if G correctly classifies Y and positive if it does not
- u(Y)
    -  vector of predictive attributes of Y
- v
    - v = Y.c
    -  classification attribute
- if G classifies Y
    - correctly is zero
    - incorrectly is positive
    - formula d^_2_(g_v_,u(Y)) - d^_2_(r_G_(Y),u(Y)) is zero
- error cost
    - associate an error cost with Y for classifies G
    - formula Cost_G_(Y) = min(M, d^_2_(g_v_, u(Y)) - d^_2_(r_g_(Y), u(Y)))
- M
    -  externally provided
- putting maximum on cost
    - to make sure that distant outliers do not have too much of an influence
-  objective function for G with respect to a given training set T
    -  sum of the costs of the instances in Y: O_T_(G) = Σ_
Y ∈T_ Cost_G_(Y )
-  negative gradient of O with respect to an exemplar vector ~g_v_ computes as :
    - P_G,v_(T)
        -  set of all instances Y in T such that Y.C = v but ~r_G_ != ~g_v_ and
Cost_G_ (Y ) < M ;
        - that is the points that are labeled v but misclassified, and have a cost less than M.
    - Q_G,v_(T)
        - set of all instances Y in T such that Y.C != v, but ~r_G_ = ~g_v_ and
Cost_G_ (Y ) < M
        - points that are classified as v but whose label is actually something else and have a cost less than M
- negative gradient of O with respect to −~g_v_ given by:
    - formula -  $ \nabla g_v_ $
    - formula - gradient g_v_(O) = 2 * Σ__Y ϵ P_G,v_(T)__(u(Y) - g_v_) + 2 * Σ__Y ϵ Q_G,v_(T)__(u(Y) - g_v_)
- giving up exmplars:
    - Intuitively, you want to move ~g_v_ toward data points that should be labelled v but are not, and away from data points that are labelled v but should be labelled something else
    - However, if a data point is too far from its proper exemplar, then we give it up (for the time being) as hopeless, and don’t consider it in the calculations.
- gradDescent:
    - driver program
    - vectors g_1_, ..., g_c_
        - first pass, they are initialized to be the centroid of their
respective categories
        - remaining passes, they will be initialized randomly
    - each attribute
        -  find the minimum and maximum value in the training set; then sample uniformly between the minimum and maximum to randomly initialize the vectors
- after classifier returned:
    - fraction of points in the training set classified correctly is computed
- predictive attributes
    -  floating point numbers
- classification attributes
    - values are single lower-case letters ‘a’ through ‘z’
