import ROOT as R
import os 
from styles import ModTDRStyle, color_dict, process_labels

R.gROOT.SetBatch()
ModTDRStyle()


file_shapes = R.TFile.Open("/work/olavoryk/tau_pog_tau_sfs/tauid_multifit/smhtt_ul/output/tight-2016postVFP-mt-2016postVFP_meas_tauid_v1-tight_vs_ele_id_es_v3/synced/htt_mt.inputs-sm-Run2016-ML.root", "read")


def plot_values():
    categories = []
    for k in file_shapes.GetListOfKeys():
        cat = k.ReadObj()
        category = cat.GetName()
        # print(category)
        categories.append(category)
    for cat in range(len(categories)):
    # for cat in range(len(["mt_DM_0", "DM1", "DM_10_11"])):
    # for cat in range(len(["mt_DM_0",])):
        shapes_list = []
        for i in range(len(file_shapes.Get(str(categories[cat])).GetListOfKeys())):
            shapes_list.append(file_shapes.Get(categories[cat]).GetListOfKeys()[i].GetName())
        print(shapes_list)

        for i in range(len(shapes_list)):
        # for i in range(len(['EMB_DM0', 'EMB_DMO_CMS_scale_temb_1prong_Run2016Down', 'EMB_DMO_CMS_scale_temb_1prong_Run2016Up'])):
            pairs = []
            if "Down" in shapes_list[i]:
                shapes_list[i][:-4] == shapes_list[i+1][:-2]
                pairs.append(shapes_list[i])
                pairs.append(shapes_list[i+1])
                nom  = pairs[0][:pairs[0].find("CMS")-1]
                pairs.append(nom)
                # print(pairs)

                R.gStyle.SetOptStat(0)
                R.gStyle.SetTitleFontSize(0.01)
                

                canv = R.TCanvas("c", "c", 1000, 950)


                pad2 = R.TPad("pad2", "pad2", 0.,0.,1,0.3)
                pad2.Draw()
                pad2.SetTopMargin(0.001)
                pad2.SetBottomMargin(0.3)
                pad2.SetGrid()

                pad1 = R.TPad("pad1", "pad1", 0.,0.3,1.,1.)
                pad1.Draw()
                pad1.SetBottomMargin(0.001)
                pad1.SetGrid()

                down_shape = file_shapes.Get(categories[cat]).Get(pairs[0])
                up_shape = file_shapes.Get(categories[cat]).Get(pairs[1])
                nominal = file_shapes.Get(categories[cat]).Get(pairs[2])

                down_mean = down_shape.GetMean()
                up_mean = down_shape.GetMean()
                nom_mean = down_shape.GetMean()


                pad1.cd()
                
                
                down_shape.SetLineColor(R.kBlue)
                up_shape.SetLineColor(R.kRed)
                nominal.SetLineColor(R.kBlack)

            

                legend = R.TLegend(0.6, 0.7, 0.9, 0.9)
                legend.SetTextSize(0.04)
                legend.AddEntry(down_shape, "down, mean: "+str(round(down_mean, 4)), "l")
                legend.AddEntry(up_shape, "up, mean: "+str(round(up_mean, 4)), "l")
                legend.AddEntry(nominal, "nominal, mean: "+str(round(nom_mean, 4)), "l")

                down_shape.SetMarkerColor(R.kBlue)
                up_shape.SetMarkerColor(R.kRed)
                nominal.SetMarkerColor(R.kBlack)


                down_shape.SetLineWidth(2)
                up_shape.SetLineWidth(2)
                nominal.SetLineWidth(2)


        
                up_shape.Draw("HIST ")
                nominal.Draw("HIST SAME")
                down_shape.Draw("HIST SAME")

                legend.Draw()

                text1 = R.TLatex(15,400+165,str(pairs[0][:-12]))
                text1.SetTextSize(0.04)
                text1.Draw()
           


                #     ratio
                pad2.cd()


                ratio_up = up_shape.Clone()
                ratio_up.Divide(nominal)

                ratio_down = down_shape.Clone()
                ratio_down.Divide(nominal)

                ratio_up.SetLineColor(R.kRed)
                ratio_down.SetLineColor(R.kBlue)


                ratio_up.GetXaxis().SetTitle("m_{#tau#tau} GeV")
                ratio_up.GetXaxis().SetTitleSize(0.12)
                ratio_up.GetXaxis().SetLabelSize(0.1)
                ratio_up.GetYaxis().SetLabelSize(0.08)

                ratio_up.GetYaxis().SetTitleOffset(0.5)
                ratio_up.GetYaxis().SetTitle("Up-Down /Nom ratio")
                ratio_up.GetYaxis().SetTitleSize(0.1)



                ratio_up.Draw()
                ratio_down.Draw("same")
                canv.Draw()
                directory = "/home/olavoryk/helper/2016UL/up_down_unc_ratio_v7/"+str(categories[cat])+"/"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                canv.SaveAs(directory+str(categories[cat])+"_"+pairs[0][:-4]+".png")

plot_values()