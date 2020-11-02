from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'HIMB0_V0Cumu_Ks_SBNeg_Mid_sysCentPlus_v2'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = False
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qwcumu_PbPb18_V0_CentBias_v2s.py'
#config.JobType.maxJobRuntimeMin = 2500
config.JobType.inputFiles = ['MC_Full_BDT250_D4.KS.weights.xml']
config.JobType.pyCfgParams = ['part=KS', 'massRange=SBNeg', 'rap=Mid']
config.Data.inputDataset = '/HIMinimumBias0/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'Automatic'
#config.Data.unitsPerJob = 8
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/PbPb2018'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/HI/PromptReco/Cert_326381-327564_HI_PromptReco_Collisions18_JSON.txt'
config.Data.publication = False
#config.Data.outputDatasetTag = ''
config.Data.useParent = True
config.Data.ignoreLocality = True
config.Site.whitelist = ['T2_US_Vanderbilt']
config.Site.storageSite = 'T2_CH_CERN'
config.Data.allowNonValidInputDataset = True
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)

