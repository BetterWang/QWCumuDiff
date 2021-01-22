from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'PAHM0_H_eta18_veto10_reverse_v2'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qwcumu_pPb16_HM0_H_eta18_v2_veto.py'
config.Data.inputDataset = '/PAHighMultiplicity0/PARun2016C-PromptReco-v1/AOD'
#config.JobType.inputFiles = ['Hijing_8TeV_dataBS.root']
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 20
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/cumu/'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/HI/Cert_285952-286496_HI8TeV_PromptReco_Pbp_Collisions16_JSON_NoL1T.txt'
config.Data.publication = False
config.JobType.allowUndistributedCMSSW = True
#config.Data.useParent = True
config.Site.storageSite = 'T2_CH_CERN'
#config.Site.ignoreGlobalBlacklist = True
##config.Data.ignoreLocality = True
##config.Site.whitelist = ['T2_CH_CERN']
##config.Data.allowNonValidInputDataset = True
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#

config.General.requestName = 'PAHM0_H_eta24_veto10_reverse_v2'
config.JobType.psetName = 'qwcumu_pPb16_HM0_H_eta24_v2_veto.py'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)


