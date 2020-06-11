from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'HIMB4_V0Cumu_H_Mid_recovery_v3'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = False
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qwcumu_PbPb18_H_Mid_v2.py'
#config.JobType.maxJobRuntimeMin = 2500
config.Data.inputDataset = '/HIMinimumBias4/HIRun2018A-04Apr2019-v1/AOD'
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/PbPb2018'
config.Data.lumiMask = 'CrabArea/crab_HIMB4_V0Cumu_H_Mid_v3/results/notFinishedLumis.json'
config.Data.publication = False
#config.Data.outputDatasetTag = ''
#config.Data.useParent = True
#config.Data.ignoreLocality = True
#config.Site.whitelist = ['T2_US_Vanderbilt']
config.Site.storageSite = 'T2_CH_CERN'
#config.Data.allowNonValidInputDataset = True
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


