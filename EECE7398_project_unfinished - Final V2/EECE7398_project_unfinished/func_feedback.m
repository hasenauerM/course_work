
% Compute control action using feedback linearization
%
% Inputs:
%       x: states
%           q1
%           q2
%           q3
%           dq1
%           dq2
%           dq3
%       alpha: Bezier coefficients for q2 and q3
%           alpha2 (1st to 5th coefficients)
%           alpha3 (1st to 5th coefficients)
%       s_params: for gait timing
%           q1_min
%           delq
%
% Outputs:
%       u: control action
%
function u = func_feedback(x,alpha,s_params)

% kp1 = 8000; %fluid walking but not good phase portrait
% kp2 = 500;
% kd1 = 60;
% kd2 = 60;

% kp1 = 10000; %very good phase portraits but snapping the neck a bit
% kp2 = 2000;
% kd1 = 60;
% kd2 = 60;

kp1 = 10000; %good mix of fluid and good phase portrait
kp2 = 2000;
kd1 = 60;
kd2 = 100;

% Seperating inputs
q = x(1:3);
dq = x(4:6);

% Get model parameters
[r,m,Mh,Mt,l,g] = func_model_params;
params = [r,m,Mh,Mt,l,g];

% Seperate Bezier coefficients
alpha2 = alpha(1:5);
alpha3 = alpha(6:10);

% Seperate s_params
q1_min = s_params(1);
q1_max = s_params(2);
delq = q1_max - q1_min;

% Gait timing variable
% Inputs:
%       q1
%       q1_min
%       delq
s = func_gait_timing(q(1), q1_min, q1_max);

% Building output function
%       y = h(x) = Hq - hd

% Get D,C,G,B matrices
% Inputs:
%       q = [q1, q2, q3]
%       dq = [dq1, dq2, dq3]
%       params = [r,m,Mh,Mt,l,g]
[D,C,G,B] = func_compute_D_C_G_B(q,dq,params);

% Defining fx and gx
fx = [dq;(D^-1)*(C*dq+G)];
gx = [zeros(3,2); (D^-1)*B];

% find y
b2 = bezier(s, 4, alpha2);
b3 = bezier(s, 4, alpha3);
h = [q(2) - b2; q(3) - b3];         
y = h;

% Calculating y_dot
dh_dx = [-1, 1, 0, 0, 0, 0; -1, 0, 1, 0, 0, 0];
dh_dx(1,1) = -d_ds_bezier(s, 4, alpha2);
dh_dx(2,1) = -d_ds_bezier(s, 4, alpha3);
Lfh = dh_dx * fx;
dy = Lfh;

%%%% PD controller
Kp = [kp1,0; 0,kp2];
Kd = [kd1,0; 0,kd2];
v = (Kd*Lfh + Kp*h);

%%%% Feedback linerization:
dLfh = func_compute_dLfh([s,delq],dq(1),[alpha2,alpha3]);
L2fh = [dLfh(:,1:3), dh_dx(:,1:3)] * fx;
LgLfh = [dLfh(:,1:3), dh_dx(:,1:3)] * gx;

% Control action that uses feedback linearization with PD controller
u = -1*(LgLfh^(-1))*(L2fh + v);

end