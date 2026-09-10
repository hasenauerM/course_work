
% Include util and autogen folders
set_path

%   f = [q10, dq10, alpha(3-5)_q2, alpha(3-5)_q3]
%       q10: pre-impact inital angle for q1
%       dq10: pre-impact inital velocity for dq1
%       alpha(3-5)_q2:
%                   3rd to 5th Bezier coefficient for q2
%       alpha(3-5)_q3:
%                   3rd to 5th Bezier coefficient for q3
%
% Manually tuned (working):
f =   [   -0.2991   -1.0383    0.3018    0.4633    0.6509    3.0918    3.0498    2.9500];

z_tot = [];
t_tot = [];

n = 5;

for i = 1:n
    
    % Simulation of a single step of ZD to using preimpact conditions
    %   applies impact first then simulates zero dynamics
    %
    % Inputs: f = [q10, dq10, alpha(3-5)_q2, alpha(3-5)_q3]
    %       q10: pre-impact inital angle for q1
    %       dq10: pre-impact inital velocity for dq1
    %       alpha(3-5)_q2:
    %                   3rd to 5th Bezier coefficient for q2
    %       alpha(3-5)_q3:
    %                   3rd to 5th Bezier coefficient for q3
    %
    % Outputs:
    %       t_sol - time (s) of zero dynamics
    %       z_sol - [q1, dq1] post impact dynamics
    %
    [t_sol, z_sol] = sim_zero_dynamics(f);
    
    f(1:2) = z_sol(end,:);
    
    z_tot = [z_tot; z_sol];


%     t_len = length(t_tot);
%     if t_len>0
%       t_sol = t_sol+t_tot(t_len);
%       t_tot = [t_tot;t_sol];
%     else
%         t_tot = t_sol;
%     end

    t_tot = [t_tot;t_sol];
    
end

figure
plot(z_tot(1,1),z_tot(1,2),'x'), hold on
plot(z_tot(:,1),z_tot(:,2))
hold off, grid on
title('Phase portrait of q_1 vd dq_1')
xlabel('q_1 (rads)')
ylabel('dq_1 (rads/s)')
legend('Start','Trajectory')


%%% addded code to try to get animation working - modifications needed
%%% still will explore during mini project 4
% s_params = [-1*f(1), f(1)];
% a1 = [-1*f(5),-1*f(4),f(3),f(4),f(5)];
% a2 = [-1*f(8)+2*f(6),-1*f(7)+2*f(6),f(6),f(7),f(8)];
% a = [a1, a2];
% 
% 
% num_zs = length(z_tot);
% X = zeros(num_zs, 6);
% for i = 1:num_zs
%     z = z_tot(i,:);
%     X(i,:) = func_map_z_x(z,a,s_params);
% end
% 
% animate_results(t_tot,X)

