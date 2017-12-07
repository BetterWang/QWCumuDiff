from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'HIMB5_Lambda_cumu_eff_v2'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qwcumu_PbPb15_ppReco_Lambda_eff_v1.py'
config.Data.inputDataset = '/HIMinimumBias5/davidlw-RecoSkim2015_pprereco_V0Cascade_Golden_v2-a2a36526d6b050b4e6f00846a47a9f83/USER'
config.JobType.inputFiles = ['Hydjet_eff_mult_v1.root']
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 20
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/cumu/'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/HI/Cert_262548-263757_PromptReco_HICollisions15_JSON_v2.txt'
config.Data.publication = False
config.Data.useParent = True
config.Site.storageSite = 'T2_CH_CERN'
config.Site.ignoreGlobalBlacklist = True
#config.Data.allowNonValidInputDataset = True
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


### HM6
config.General.requestName = 'HIMB6_Lambda_cumu_eff_v2'
config.Data.inputDataset = '/HIMinimumBias6/davidlw-RecoSkim2015_pprereco_V0Cascade_Golden_v2-a2a36526d6b050b4e6f00846a47a9f83/USER'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


### HM7
config.General.requestName = 'HIMB7_Lambda_cumu_eff_v2'
config.Data.inputDataset = '/HIMinimumBias7/davidlw-RecoSkim2015_pprereco_V0Cascade_Golden_v2-a2a36526d6b050b4e6f00846a47a9f83/USER'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


