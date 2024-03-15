import ROOT as R
import os 

R.gROOT.SetBatch()
import json


def in_out_put():
    with open('input_output_config.json') as f:
        d = json.load(f)
        input_file = d['input_file']
        out_folder = d['output_folder']

        return input_file, out_folder


def plot_values():
    categories = []
    input_file = in_out_put()[0]
    out_fold = in_out_put()[1]
    file_shapes = R.TFile(input_file)
    for k in file_shapes.GetListOfKeys():
        cat = k.ReadObj()
        category = cat.GetName()
        # print(category)
        categories.append(category)
    for cat in range(len(categories)): # categories ["mt_DM_0", "DM1", "DM_10_11"]
        shapes_list = []
        for i in range(len(file_shapes.Get(str(categories[cat])).GetListOfKeys())):
            shapes_list.append(file_shapes.Get(categories[cat]).GetListOfKeys()[i].GetName())
        print(shapes_list)

        for i in range(len(shapes_list)): # shapes list ['EMB_DM0', 'EMB_DMO_CMS_scale_temb_1prong_Run2016Down', 'EMB_DMO_CMS_scale_temb_1prong_Run2016Up']
            pairs = []
            if "Down" in shapes_list[i]:
                shapes_list[i][:-4] == shapes_list[i+1][:-2]
                pairs.append(shapes_list[i])
                pairs.append(shapes_list[i+1])
                nom  = pairs[0][:pairs[0].find("CMS")-1]
                pairs.append(nom)

                R.gStyle.SetOptStat(0)
                R.gStyle.SetTitleFontSize(0.05)
                

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
                directory = out_fold+str(categories[cat])+"/"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                canv.SaveAs(directory+str(categories[cat])+"_"+pairs[0][:-4]+".png")

if __name__ == '__main__':
    plot_values()