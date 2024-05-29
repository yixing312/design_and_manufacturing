% 通过Ansys和Python端分析器得到的数据进行拟合

clear;
close all;
clc;

file_path = '2024-05-07 19_27_22';
%% 加载数据
%数据路径
ans_path = ['../data/' file_path '/ans' '.txt'];
task_path = ['../data/' file_path '/task' '.txt'];
new_task_path = ['../data/new_task' '2' '.txt'];%洗数据

% 打开原始数据文件
fid = fopen(task_path, 'r');
if fid == -1
    error('无法打开文件 %s', task_path);
end
% 创建或清空新文件
newFid = fopen(new_task_path, 'w');
if newFid == -1
    fclose(fid); % 关闭原始文件
    error('无法创建或写入文件 %s', new_task_path);
end

% 读取文件并处理数据
while ~feof(fid)
    line = fgetl(fid); % 读取一行
    if isempty(line)
        continue;
    end
    
    % 提取方括号内的数据
    startIdx = strfind(line, '[');
    endIdx = strfind(line, ']');
    % if ~isempty(startIdx)
    %     dataStr=line(startIdx+1:end);
    %     dataStr = strtrim(dataStr); % 去除首尾空白字符
    %     dataStr = strsplit(dataStr, {' '}); % 分割字符串
    %     dataStr = dataStr(~isspace(dataStr)); % 移除空格
    %     data = str2double(dataStr); % 转换为数字
    %     % 将数据写入新文件
    %     fprintf(newFid, '%g %g %g %g %g ', data);
    % end
    % if ~isempty(endIdx)
    %     dataStr=line(1:endIdx-1);
    %     dataStr = strtrim(dataStr); % 去除首尾空白字符
    %     dataStr = strsplit(dataStr, {' '}); % 分割字符串
    %     dataStr = dataStr(~isspace(dataStr)); % 移除空格
    %     data = str2double(dataStr); % 转换为数字
    %     % 将数据写入新文件
    %     fprintf(newFid, '%g\n', data);
    % end

    if ~isempty(startIdx)
        dataStr=line(startIdx+1:end-1);
        dataStr = strtrim(dataStr); % 去除首尾空白字符
        dataStr = strsplit(dataStr, {' '}); % 分割字符串
        dataStr = dataStr(~isspace(dataStr)); % 移除空格
        data = str2double(dataStr); % 转换为数字
        % 将数据写入新文件
        fprintf(newFid, '%g %g %g %g %g %g\n', data);
    end
end

% 关闭文件
fclose(fid);
fclose(newFid);
% 输出成功信息
disp('数据已成功写入新文件！');

concentricity = importdata(ans_path);
preload = importdata(new_task_path);

data=[preload concentricity];

data =sortrows(data,7);
fprintf(file_path+"最优：\n预紧力：");
disp(data(1,1:6));
fprintf("同轴度：");
disp(data(1,7));
%% 拟合

model = fitlm(preload,concentricity,'quadratic');
% model = fitlm(preload,concentricity,'poly111111')
% disp(model.VariableInfo);
% model.predict([5000 5000 5000 5000 5000 5000]);%预测
%% 绘图

figure(1)
plotEffects(model);

figure(2)
for i = 1:6
    fig = subplot(2,3,i);
    plotPartialDependence(model,i,"Conditional","absolute");
    y= model.VariableInfo.Range{7};
    fig.YTick = linspace(y(1),y(2),8);
    ylim(model.VariableInfo.Range{7});
    xlim(model.VariableInfo.Range{i});
    title(['部分依赖图—F_' num2str(i)],'FontSize',14,'FontName','霞鹜文楷等宽');
    grid on
    % grid minor
    % set(findobj('Type','line'),'LineWidth',2);
    ylabel('同轴度 [mm]','FontSize',12,'FontName','霞鹜文楷等宽');
    xlabel(['F_' num2str(i) '[N]'],'FontSize',12,'FontName','霞鹜文楷等宽','Interpreter','tex');
end 
% legend('1','2','3')
% figure(3)
% plot(model);
% plotPartialDependence(model,[1 2]);
% xlabel('F_1 [N]','FontSize',12,'FontName','霞鹜文楷等宽','Interpreter','tex');
% ylabel('F_2 [N]','FontSize',12,'FontName','霞鹜文楷等宽','Interpreter','tex');
% zlabel('同轴度 [mm]','FontSize',12,'FontName','霞鹜文楷等宽','Interpreter','tex');

figure(4);
hold on
for i = 1:6
    plotPartialDependence(model,i);
    % set(findobj('Type','line'),'LineWidth',2);
end
legend(['F_1';'F_2';'F_3';'F_4';'F_5';'F_6'],'Interpreter','tex');
title('单变量影响图','FontSize',14,'FontName','霞鹜文楷等宽');
grid on
% grid minor
ylabel('同轴度 [mm]','FontSize',12,'FontName','霞鹜文楷等宽');
xlabel('F [N]','FontSize',12,'FontName','霞鹜文楷等宽','Interpreter','tex');
hold off

% figure(5)
% for i = 1:6
%     subplot(2,3,i);
%     data = sortrows(data,i);
%     [up_bound,~] = find(data(:,i)>4950,1,'first');
%     if isempty(up_bound)
%         up_bound = length(data(:,i));
%     end
%     hold on
%     scatter(data(1:up_bound,i),data(1:up_bound,7),'blue');
%     scatter(data(up_bound:end,i),data(up_bound:end,7),'red');
%     hold off
% end
% plotSlice(model);
