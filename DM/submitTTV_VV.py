path2xml="$SFRAME_DIR/../BatchSubmission/xmls_ttV_VV"
path2tmp="$SFRAME_DIR/../DM/AnalysisTemp"
outDir="$SFRAME_DIR/../DM/AnalysisOutput"
jobName="DMAnalysisJob"
cycleName="DMAnalysis"
outputLevel="WARNING"
nEventsMax=-1
nProcesses=1
nFiles=20
hCPU="06:00:00"
hVMEM="1500M"
postFix = ""


dataSets = []
listDir = "../BatchSubmission/lists_ttV_VV"
for d in ["TTWJetsToQQ","TTZToQQ","WZTo1L3Nu","WZTo3LNu"]:
    dataSets.append([d, open(listDir+"/"+d+".txt").read().splitlines()])


userItems = [
    ["IsData", "false"],
    ["IsSignal", "false"],
]

jobOptionsFile2=open("AnalysisOptions.py", 'r')
command2=""
for i in [o for o in jobOptionsFile2.readlines()]:
  if ("#E" + "nd") in i : break
  command2+=i
jobOptionsFile2.close()
exec command2
userItems += AddUserItems


inputTrees=["ntuplizer/tree"]
outputTrees=["tree"]
