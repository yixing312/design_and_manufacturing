import os
import wbjn

model = ExtAPI.DataModel.Project.Model
geom = model.Geometry
mesh = model.Mesh
connections = model.Connections
materials = model.Materials
analysis = model.Analyses[0]
solution = analysis.Solution
cmd = "returnValue(GetUserFilesDirectory())"
user_dir = wbjn.ExecuteCommand(ExtAPI, cmd)

bolt_pretension_ids = [209, 211, 213, 215, 217, 219]
file_path = user_dir + "/test.txt"
# TODO 该路径与py端不一致
# py端为 "../data/task_queue.txt"

epoch = 2
countdown = epoch


def Ansys_task(current_task):
    global analysis
    # set forces
    for i in range(6):
        Id = bolt_pretension_ids[i]
        bolt_pretension = DataModel.GetObjectById(Id)
        bolt_pretension.Preload.Inputs[0].DiscreteValues = [Quantity("1[s]")]
        bolt_pretension.Preload.Output.DiscreteValues = [
            Quantity(current_task[i] + "[N]")
        ]

    # calculate the solution
    analysis.Solve()
    for analysis in ExtAPI.DataModel.AnalysisList:
        # Get All direction Deformation Objects in all the Analyses in the Tree
        DirectionDeformationResults = [
            child
            for child in analysis.Solution.Children
            if child.DataModelObjectCategory
            == DataModelObjectCategory.DirectionalDeformation
        ]
        for result in DirectionDeformationResults:
            result.Activate()
            filename = (
                user_dir
                + "/"
                + Model.Analyses[0].Name
                + str(countdown)
                + " - "
                + result.Name
                + ".txt"
            )
            # TODO 该文件路径与py端不一致
            # py端为 "../data/Ansys/" + str(task) + "/" + result.Name + ".txt"
            # 其中 task 的每个元素为 float 类型，这里是string类型，可能需要转换一下
            result.ExportToTextFile(filename)


while countdown > 0:
    if os.path.exists(file_path):
        if os.path.getsize(file_path) == 0:
            break
        with open(file_path, "r", encoding="utf8") as f:
            # 如果文件为空，退出循环

            for line in f:
                task = line[1:-2].Split()
                Ansys_task(task)

            print("Script has completed!")
            print("The end")
        # delet the file
        os.remove(file_path)
        countdown -= 1
    else:
        # TODO 这里建议放个一秒的延时，避免持续抢占文件权限
        continue
