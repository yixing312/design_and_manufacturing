import os
import wbjn
import time

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
file_path = 'E:/ansysFiles/design_and_manufacturing/data'
task_path = file_path + '/task_queue.txt'

endFlag = 1


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
                file_path
                + "/Ansys_data/"
                + ",".join([str(i) for i in current_task])
                + "/"
                + Model.Analyses[0].Name
                + " - "
                + result.Name
                + ".txt"
            )
            result.ExportToTextFile(filename)


while 1:
    if os.path.exists(file_path + '/task_queue.txt'):
        with open(file_path + '/task_queue.txt', 'r') as f:
            # if read end then end
            lines = f.readlines()
            if lines[0]=="end":
                break
            for line in lines:
                task = line[0:-1].Split(",")
                Ansys_task(task)
        # delet the file
        os.remove(file_path + '/task_queue.txt')
    else:
        time.sleep(0.5)
        continue
        
