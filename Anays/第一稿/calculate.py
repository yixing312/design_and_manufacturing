import wbjn
import os

model=ExtAPI.DataModel.Project.Model
geom = model.Geometry
mesh= model.Mesh
connections=model.Connections
materials =model.Materials
analysis =model.Analyses[0]
solution =analysis.Solution
cmd = 'returnValue(GetUserFilesDirectory())'
user_dir = wbjn.ExecuteCommand(ExtAPI, cmd)

bolt_pretension_ids = [209, 211, 213, 215, 217, 219]
file_path = user_dir + "/test.txt"
forces = []
epoch = 2
countdown = epoch

while countdown > 0:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            # input forces
            for line in f:
                nums = line.Split()
                for num in nums:
                    forces.append(num)
            # set forces
            count = 0
            for id in bolt_pretension_ids:
                bolt_pretension = DataModel.GetObjectById(id)
                bolt_pretension.Preload.Inputs[0].DiscreteValues = [Quantity('1[s]')]
                bolt_pretension.Preload.Output.DiscreteValues = [Quantity(forces[count] + '[N]')]
                count += 1
            # calculate the solution
            analysis.Solve() 
            for analysis in ExtAPI.DataModel.AnalysisList:
                #Get All direction Deformation Objects in all the Analyses in the Tree
                DirectionDeformationResults = [child for child in analysis.Solution.Children if child.DataModelObjectCategory == DataModelObjectCategory.DirectionalDeformation]
                for result in DirectionDeformationResults:
                    result.Activate()
                    filename = user_dir + "/" + Model.Analyses[0].Name + str(countdown) + " - " + result.Name + ".txt"
                    result.ExportToTextFile(filename)
            print("Script has completed!")
            print("The end")
        # delet the file
        os.remove(file_path)
        countdown -= 1
    else:
        continue
