from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'HIMB4_V0Tree_v9'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = False
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qw_PbPb18_MB_V0Tree_v6.py'
#config.JobType.maxJobRuntimeMin = 2500
#config.JobType.inputFiles = ['Hydjet_PbPb_eff_v1.root', 'Hydjet_ppReco_v5_loose.root']
config.Data.inputDataset = '/HIMinimumBias4/qwang-V0Skim_v3-9d53152409b8a9b6fb15042030d9bf69/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/PbPb2018'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/HI/PromptReco/Cert_326381-327560_HI_PromptReco_Collisions18_JSON.txt'
config.Data.publication = False
#config.Data.outputDatasetTag = ''
config.Data.useParent = True
config.Data.ignoreLocality = True
config.Site.whitelist = ['T2_US_Vanderbilt']
config.Site.storageSite = 'T2_CH_CERN'
config.Data.allowNonValidInputDataset = True
config.JobType.allowUndistributedCMSSW = True
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#

config.General.requestName = 'HIMB2_V0Tree_WrongSign_v9'
config.Data.inputDataset = '/HIMinimumBias2/qwang-V0SkimWrongSign_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)

#
#config.General.requestName = 'HIMB19_V0Tree_v9'
#config.Data.inputDataset = '/HIMinimumBias19/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#config.Data.lumiMask = 'run327237.txt'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.JobType.psetName = 'qw_PbPb18_MB_V0Tree_noAPCut_v6.py'
#config.General.requestName = 'HIMB19_V0Tree_noAPCut_v9'
#config.Data.inputDataset = '/HIMinimumBias19/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#config.Data.lumiMask = 'run327237.txt'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
